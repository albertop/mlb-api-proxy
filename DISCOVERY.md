# MLB API Proxy — Discovery (Etapa 1)

> Documento de descubrimiento del proyecto. Fotografía del estado actual antes de la
> revisión de código y del trabajo de resiliencia + integración de Statcast (Baseball Savant).
>
> Fecha: 2026-07-16

---

## 1. Qué es el proyecto

Un **proxy HTTP en FastAPI** que se pone delante de la API pública de MLB
(`https://statsapi.mlb.com`). No implementa lógica de negocio propia: recibe una petición,
la reenvía al upstream de MLB, y sobre la respuesta aplica algunas transformaciones antes de
devolverla al cliente.

**Valor que aporta el proxy (más allá de reenviar):**

1. **Autenticación de acceso** — exige un header `X-API-Key` que debe coincidir con
   `PROXY_API_KEY`. El upstream de MLB queda oculto tras esta capa.
2. **Normalización XML → JSON** — detecta respuestas XML (por `Content-Type` o por un `<`
   inicial) y las convierte a JSON con `xmltodict`.
3. **Traducción de nombres de estadísticas** — renombra campos de stats de MLB
   (`homeRuns` → `HR`, `battingAverage` → `AVG`, …) usando un diccionario de ~cientos de
   entradas (`stats_translations.py`). Búsqueda case-insensitive.
4. **Normalización de nulos** — convierte valores "vacíos" de MLB (`".---"`, `"-"`, `"-1"`,
   `""`, …) a `null`.
5. **Limpieza de copyright** — elimina el campo `copyright` de las respuestas.
6. **Endpoints auxiliares** — `/metric_abbreviation` y `/abbrev_description_spanish` para
   consultar abreviaturas y descripciones en español.
7. **Observabilidad básica** — `x-request-id` por petición, manejadores de error
   centralizados, y un `/health` que verifica también el upstream.

---

## 2. Arquitectura

```
Cliente ──X-API-Key──► FastAPI (main.py)
                          │
                          ├─ middleware: x-request-id
                          ├─ exception handlers (HTTP / validation / 500)
                          ├─ /health, /metric_abbreviation, /abbrev_description_spanish
                          │
                          └─ 25 routers (routers/*.py)  ~150 endpoints GET
                                   │
                                   └─ forward_get()  ◄── núcleo (proxy.py)
                                          │  require_api_key
                                          │  build_upstream_headers
                                          │  httpx.AsyncClient.get(upstream)
                                          │  should_parse_xml → xmltodict
                                          │  strip_copyright
                                          │  normalize_null_values
                                          │  translate_stat_fields
                                          ▼
                                   statsapi.mlb.com
```

### Componentes clave

| Archivo | Rol |
|---|---|
| `api-service/main.py` | Construye la app, registra routers, middleware, exception handlers, `/health`. |
| `api-service/proxy.py` | **Núcleo.** `Settings` (pydantic-settings), `forward_get`, auth, transformaciones. |
| `api-service/stats_translations.py` | Diccionario de traducción de stats + helpers (`metric_abbreviation`, `abbrev_description_spanish`). ~1000+ líneas. |
| `api-service/routers/*.py` | 25 routers temáticos. Cada endpoint es un wrapper delgado sobre `forward_get`. |

### Los routers (25)

`attendance, awards, broadcast, conference, division, draft, games, game_pace, high_low,
job, league, milestones, misc, people, schedule, season, sports, standings, stats, teams,
transactions, uniforms, venues` (+ `__init__`).

Todos siguen el **mismo patrón repetido**: cada endpoint declara
`request: Request, x_api_key: Optional[str] = Header(None)` y hace
`return await forward_get(request, "<path>", x_api_key)`. Es boilerplate puro, replicado
~150 veces.

---

## 3. Configuración

Vía `pydantic-settings` (`.env` + variables de entorno). Definidas en `Settings` (`proxy.py`):

| Variable | Default | Uso |
|---|---|---|
| `MLB_BASE_URL` | `https://statsapi.mlb.com` | Upstream. |
| `PROXY_API_KEY` | *(requerida)* | Clave que exige el proxy a sus clientes. |
| `APP_VERSION` | `0.1.0` | Versión reportada. |
| `LOG_LEVEL` | `INFO` | Nivel de logging. |
| `UPSTREAM_BEARER_TOKEN` | `None` | Auth opcional hacia el upstream. |
| `UPSTREAM_BASIC_AUTH` | `None` | Auth básica opcional hacia el upstream. |
| `UPSTREAM_TIMEOUT_SECONDS` | `30.0` | Timeout de la petición al upstream. |

> ⚠️ **Deriva de configuración detectada:** `test/conftest.py` fija variables que **no
> existen** en `Settings` (`MLB_API_BASE_URL`, `MLB_API_KEY`, `REQUIRE_KEY`,
> `STRIP_COPYRIGHT`, `ENABLE_CACHE`, `CACHE_TTL`, `REQUEST_TIMEOUT`). Sugiere que hubo un
> diseño previo con caché/flags que ya no existe en el código, o tests desalineados. A revisar.

---

## 4. Testing

Framework: **pytest + pytest-asyncio + respx** (mock del upstream httpx).

```
test/
├── conftest.py            fixtures compartidos, carga de response-examples
├── contract/              (vacío — solo __init__)
├── integration/           test_end_to_end.py
├── smoke/                 test_deployment.py (contra sistema vivo)
└── unit/
    ├── routers/           un test_*.py por cada router (22 archivos)
    ├── test_critical_flows.py   (~1000 líneas)
    └── ...
```

- `pytest.ini` configura cobertura (`--cov=api-service`), markers (`unit, integration,
  contract, smoke, slow`), `asyncio_mode = auto`, timeout 300s.
- Existe `docs/response-examples/` con respuestas reales de MLB por endpoint, usadas como
  fixtures.
- Hay artefactos de cobertura versionados en el repo (`coverage.xml`, `htmlcov/`).

---

## 5. Despliegue

- **Dockerfile** multi-stage (builder + slim), Python 3.12, usuario no-root, healthcheck,
  uvicorn con `--workers ${WORKERS}` (default 4).
- **docker-compose.yml** orientado a **Portainer**: usa imagen pre-construida
  (`mlb-api-proxy:1.2026.8`), publica `3002:8000`, límites de recursos (2 CPU / 1 GB),
  red externa `backend`, DNS fijos.
- Scripts de build/deploy en `utils/` (`build_and_save_image.ps1`,
  `deploy_mlb_api_proxy_image.sh`), e imágenes `.tar` en `docker_images/`.
- Documentación de despliegue: `PORTAINER_DEPLOYMENT.md`.

> Nota: `APP_VERSION` tiene defaults inconsistentes (`0.1.0` en código/Dockerfile final vs
> `1.2026.x` en el tag de la imagen y compose).

---

## 6. Documentación existente

Abundante, en la raíz y en `docs/`:

- Raíz: `DELIVERY_SUMMARY.md`, `IMPLEMENTATION_CHECKLIST.md`, `IMPLEMENTATION_GUIDE.md`,
  `RESPONSE_COLLECTION_GUIDE.md`, `VALIDATION_REPORT.md`, `VALIDATION_SUMMARY.md`,
  `PORTAINER_DEPLOYMENT.md`.
- `docs/`: `MLB_API_Documentation.{md,html}`, `mlb_api_spec.json` (OpenAPI), catálogo de
  respuestas (`API_RESPONSE_CATALOG.md`), PDFs de referencia (GUMBO, Lookup Values), y
  `response-examples/` con JSON reales por endpoint.

---

## 7. Herramientas / calidad de código (estado actual)

| Aspecto | Estado |
|---|---|
| Gestor de dependencias | `requirements.txt` (duplicado en raíz y en `api-service/`). |
| **Linter / formatter** | ❌ **No hay ruff, black, flake8 ni mypy.** No hay `pyproject.toml`. |
| Type checking | ❌ No configurado (hay type hints parciales en el código). |
| Pre-commit hooks | ❌ No hay. |
| CI/CD | ❌ No se observa (no es repo git, no hay workflows). |
| Control de versiones | ⚠️ El directorio **no es un repositorio git**. |

---

## 8. Observaciones para la Etapa 1 (resiliencia) — resumen

Estos puntos se profundizarán en el **code review**. Aquí solo se listan como hallazgos del
discovery:

**Resiliencia / rendimiento**
1. Se crea un `httpx.AsyncClient` **nuevo por cada petición** (en `forward_get` y en
   `/health`). No hay pool de conexiones reutilizable → coste por request y menos resiliencia
   bajo carga.
2. **Sin reintentos, sin circuit breaker, sin backoff** ante fallos del upstream.
3. **Sin caché** (los tests aluden a un caché que no existe en el código).
4. **Sin rate limiting** propio.

**Corrección / riesgo de datos**
5. `normalize_null_values` convierte `""`, `"-"`, `"-1"` a `null` de forma **global y
   recursiva**. Riesgo de corromper datos legítimos (p. ej. un `-1` válido, o un string vacío
   con significado).
6. `translate_stat_fields` renombra claves **en toda la respuesta** por coincidencia de
   nombre; puede renombrar claves que no son stats si colisionan con el diccionario.

**Mantenibilidad**
7. ~150 endpoints son boilerplate idéntico; una firma/patrón compartido (o generación) los
   reduciría drásticamente.
8. Deriva entre `conftest.py` y `Settings` (variables inexistentes).
9. Ausencia total de tooling de calidad (ruff, mypy, formato).

---

## 9. Etapa 2 (Statcast / Baseball Savant) — punto de partida

- **No hay integración con Baseball Savant / Statcast todavía.** Las únicas menciones de
  "statcast/savant" están en documentación (`docs/API_RESPONSE_CATALOG.md`,
  `MLB_API_Documentation.md`), no en código.
- Baseball Savant expone datos vía endpoints CSV/JSON distintos a `statsapi.mlb.com`
  (p. ej. `baseballsavant.mlb.com/statcast_search/csv`). La arquitectura actual asume **un
  solo upstream** (`BASE_URL`), por lo que integrar Savant requerirá:
  - Soportar múltiples upstreams / un cliente dedicado a Savant.
  - Manejo de respuestas CSV (hoy solo XML y JSON).
  - Probablemente caché (las consultas de Statcast son pesadas y lentas).

Estos requisitos refuerzan el trabajo de la Etapa 1 (pool de conexiones, caché, reintentos,
soporte multi-formato).

---

## 10. Inventario rápido

- **Lenguaje:** Python 3.12
- **Framework:** FastAPI + uvicorn
- **Cliente HTTP:** httpx (async)
- **Endpoints:** ~150 GET sobre 25 routers
- **Líneas de código (routers + proxy + translations):** ~1.900 en routers, ~1.000+ en
  translations
- **Tests:** unit (por router) + integration + smoke; ~2.800 líneas
- **Despliegue:** Docker + Portainer (puerto 3002→8000)
- **Upstream:** `https://statsapi.mlb.com`
```
