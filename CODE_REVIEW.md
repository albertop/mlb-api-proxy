# MLB API Proxy — Code Review (Etapa 1)

> Revisión de código enfocada en **mejores prácticas, resiliencia y correctitud**, como
> preparación para (a) construir un website sobre este proxy y (b) integrar Statcast /
> Baseball Savant.
>
> Fecha: 2026-07-16 · Complementa a [`DISCOVERY.md`](DISCOVERY.md)

---

## 0. TL;DR

El proxy está **bien estructurado y limpio** para lo que hace: routers delgados, un núcleo
único (`forward_get`), manejo de errores centralizado, healthcheck que valida upstream y
Docker con usuario no-root. La base es sólida.

Para hacerlo "lo más resiliente posible" antes del website, los tres cambios de mayor impacto
son:

1. **Reutilizar un cliente httpx** (hoy se crea uno nuevo por request) → pool de conexiones.
2. **Añadir reintentos + timeouts granulares + (opcional) circuit breaker** hacia el upstream.
3. **Acotar las transformaciones de datos** (`normalize_null_values`, `translate_stat_fields`)
   que hoy actúan de forma global y pueden corromper/renombrar datos legítimos.

Ya se ha **configurado ruff + mypy** (`pyproject.toml`) y aplicado las correcciones
automáticas seguras al código de producción (`api-service/` pasa `ruff check` limpio).

---

## 1. Tooling aplicado en esta revisión

- ✅ **`pyproject.toml`** nuevo con `ruff` (lint + format) y `mypy`, más `[project]` y extras `dev`.
- ✅ **ruff** ejecutado sobre `api-service/`: de **202 hallazgos → 0**. Correcciones aplicadas:
  ordenamiento de imports, `Optional[X]` → `X | None` (PEP 604), whitespace, f-strings sin
  placeholder, imports sin usar.
- ✅ **4 arreglos manuales** que ruff marcó pero no auto-corrige:
  - `proxy.py` — `raise HTTPException(...) from exc` en los dos `except` (encadenado de
    excepciones, regla `B904`).
  - `stats_translations.py` — **clave duplicada** `"passedBalls"` eliminada (regla `F601`).
  - `main.py` — import de `routers` movido arriba (regla `E402`).
- ⚠️ **mypy**: 2 avisos menores restantes (ver §5), ambos de bajo riesgo.
- ⚠️ **Tests**: 239 pasan, **1 falla pre-existente** (no introducido aquí) — ver §4.1.

> Nota: las correcciones automáticas se aplicaron **solo a `api-service/`** (código que se
> despliega). Los archivos de `test/` y utilitarios de raíz tienen ~400 hallazgos de estilo
> pendientes; se pueden limpiar con `ruff check test --fix && ruff format test` cuando quieras
> (recomiendo hacerlo bajo control de versiones).

---

## 2. Hallazgos de RESILIENCIA (prioridad Etapa 1)

> **Estado (2026-07-16):** R1, R2, R3 (+ R3.1 optimización de bytes), R5 y R6 **implementados y
> verificados end-to-end en producción** (`10.0.0.39`, imagen `1.2026.10`). Suite completa:
> **290 pasan, 0 fallan**. R4 descartado (un solo cliente).

### ✅ R1 — Cliente httpx creado por cada petición (sin pool de conexiones) — HECHO
`proxy.py::forward_get` y `main.py::health_check` hacen
`async with httpx.AsyncClient(...) as client:` **dentro de cada request**. Esto:
- Abre/cierra conexiones TCP+TLS en cada llamada → latencia y CPU extra.
- Impide keep-alive y reutilización de conexiones al upstream.
- Bajo carga (un website haciendo muchas llamadas) degrada notablemente.

**Recomendación:** un **único `AsyncClient` compartido** con `limits` de pool, creado en el
`lifespan` de FastAPI y reutilizado. Ejemplo:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=httpx.Timeout(UPSTREAM_TIMEOUT_SECONDS, connect=5.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    yield
    await app.state.http.aclose()

app = FastAPI(title="MLB API Proxy", version=settings.app_version, lifespan=lifespan)
```

Luego `forward_get` usa `request.app.state.http` en vez de crear uno nuevo.

### ✅ R2 — Sin reintentos ni backoff ante fallos transitorios del upstream — HECHO
Un único fallo de red o un 5xx pasajero del upstream se propaga como 502 al cliente. Para un
website de cara al usuario esto es frágil.

**Recomendación:** reintentos con backoff exponencial para errores idempotentes (GET) y
códigos 502/503/504/timeout. Con httpx se puede vía `httpx.AsyncHTTPTransport(retries=n)`
(reintenta solo errores de conexión) o una capa propia con `tenacity`. Distinguir:
- Reintentables: timeouts, ConnectError, 502/503/504.
- No reintentables: 4xx (excepto 429, que debe respetar `Retry-After`).

### ✅ R3 — Sin caché — HECHO (in-process con cachetools + single-flight)
No hay caché pese a que `conftest.py` referencia flags (`ENABLE_CACHE`, `CACHE_TTL`) que **no
existen** en `Settings` (evidencia de un diseño anterior perdido). Muchos endpoints de MLB son
altamente cacheables (equipos, venues, tablas de lookup, standings). Para el website esto
reduce latencia y protege al upstream.

**Implementado:** caché in-process con `cachetools.TTLCache` (una por tier de TTL, acotada por
`CACHE_MAXSIZE`), **TTL por tipo de endpoint** (referencia 6h / semi-dinámico 5min / live sin
caché) vía `cache_ttl_for_path`, y **single-flight** (`_coalesce`) para evitar cache stampede.
Flag `ENABLE_CACHE` (on por defecto; off en tests). `WORKERS` bajado a 2 (caché es por worker).
Pendiente/futuro: respetar `Cache-Control` del upstream; Redis si algún día se necesita caché
compartido entre workers. **Etapa 2 (Statcast):** este caché será clave por el peso de esas
consultas.

#### ✅ R3.1 — Optimización: cachear bytes ya serializados (no el dict)
**Hallazgo (medido en producción):** el caché guardaba el `dict` transformado, así que cada
cache hit re-serializaba el JSON (`json.dumps`) en cada petición. Para respuestas grandes
(`/api/v1/teams` = 547KB) ese `json.dumps` repetido costaba ~190ms de *serve time* por hit.

**Implementado:** `FetchResult` ahora lleva `content: bytes` (JSON serializado **una sola vez**
en `_fetch_upstream`, con los mismos parámetros que Starlette → bytes idénticos), `media_type` e
`is_json`. `_build_response` emite los bytes directo (`Response(content=bytes)`), sin
re-serializar. Beneficio extra: los bytes ocupan menos memoria que el dict equivalente.

**Resultado (verificado en `10.0.0.39`, imagen `1.2026.10`):** serve time de un cache hit de
547KB pasó de **~190ms → ~15ms TTFB** (~13x; ~5ms medido en localhost sin RTT de red). Sin
regresión: 290 tests en verde, bytes de respuesta idénticos. Tests:
`test_cache.py` (coalescing devuelve `content` en bytes).

### ❌ R4 — Sin rate limiting propio — DESCARTADO (decisión)
El proxy tendrá un **único cliente** (el website propio), no es una API multi-tenant pública.
El rate limiting no aporta en este contexto. **Descartado.**

### ✅ R5 — Timeout único y grueso — HECHO
`UPSTREAM_TIMEOUT_SECONDS=30` aplica como timeout total. Un `connect` timeout separado y más
corto (p. ej. 5 s) detecta upstream caído más rápido sin penalizar respuestas lentas legítimas.
(Incluido en el ejemplo de R1.)

### ✅ R6 — `/health` duplica la lógica de cliente — HECHO
El healthcheck crea su propio `AsyncClient`. Debería reutilizar el cliente compartido (R1) para
que el health refleje el estado real del pool de conexiones que usan las peticiones.

---

## 3. Hallazgos de CORRECTITUD / RIESGO DE DATOS

> **Estado (2026-07-16):** C1 **verificado — se mantiene** (no es bug). C2 reenfocado a
> auditoría de correctitud: **hecho** (bugs corregidos, suite 100% verde: 281 pasan).

### ✅ C1 — `normalize_null_values` — VERIFICADO, se mantiene
```python
NULL_LIKE_VALUES = {".---", "-.---", "-.--", "-", "-1", ""}
```
**Verificado empíricamente contra las respuestas reales de MLB:** el token `"-1"` aparece 38
veces, todas como `birthStateProvince`/`deathStateProvince` = **centinela de null de MLB**
(persona sin estado/provincia). Los tokens `.---`/`-.--` son los nulls de rate-stats (ERA/AVG
sin denominador). Convertirlos a `null` es **correcto y mejora el dato**. Nota técnica: solo
afecta strings; los números JSON (`-1` entero) no se tocan. **Decisión: no cambiar.** Único
miembro discutible: `""`→null (0 casos hoy, inofensivo).

### ✅ C2 — Auditoría de correctitud de las traducciones — HECHO
Se decidió que la traducción a abreviaturas es el comportamiento **deseado** (el website es el
único consumidor y no espera nombres MLB). El foco pasó a **verificar que las traducciones sean
correctas**. Auditoría completa (ver `stats_translations.py` y `test/unit/test_translations.py`):
- 🔴 **`putOuts`→"Outs"** corregido a **"PO"** (era incorrecto y colisionaba con `outs`).
- 🟠 **10 abreviaturas sin español** (AB, ER, RBI, WP, GOuts, PpInn, PpPA, SaveOpp, SwingMisspct,
  Swstrpct) → añadidas.
- 🟠 **4 claves español huérfanas/typo** (`GOouts`, `SwingMisspctSwstrpct`, `PutOuts`, `XBH`) →
  corregidas/eliminadas.
- 🟠 **Claves genéricas estructurales** (`games`, `batting`, `fielding`, `baseRunning`,
  `positional`, `replacement`, `streak`) → **eliminadas** del diccionario: como claves sueltas
  renombraban secciones estructurales de la respuesta (p. ej. `dates[].games` del schedule
  pasaba a `G`; boxscore `team.batting`→`Batting`).
- 🟡 **`strikesoutsToWalks`** (typo) → `strikeoutsToWalks`.
- 🟡 **`_validate_translations()`** estaba roto (marcaba alias intencionales como duplicados,
  siempre fallaba) → reescrito como `validate_translations()`: comprueba coherencia
  abreviatura↔español, con test permanente.

### ✅ C3 — `strip_copyright` solo mira el nivel raíz — HECHO
Ahora es **recursivo**: elimina `copyright` en cualquier nivel de la respuesta. Test:
`test_proxy_transform.py::TestStripCopyright`.

### ✅ C4 — `should_parse_xml` puede tener falsos positivos — HECHO
Cuando se infiere XML por el `<` inicial (sin Content-Type XML), ahora se **loguea el
Content-Type real** para depurar falsos positivos (p. ej. una página HTML de error).

---

## 4. Hallazgos de TESTING

### ✅ 4.1 — Test pre-existente en conflicto con la feature de traducción — HECHO
`test_award_recipients_with_stats` esperaba `homeRuns` y `test_get_game_schedule_flow` esperaba
`games`. Alineados con el comportamiento deseado: el primero ahora espera `HR`; el segundo se
arregló al quitar `games` del diccionario (era una clave estructural). **Suite 100% verde.**

### ✅ 4.2 — Deriva entre `conftest.py` y `Settings` — HECHO
`conftest.py` ahora solo fija campos reales de `Settings` (`MLB_BASE_URL`, `PROXY_API_KEY`,
`LOG_LEVEL`, `ENABLE_CACHE=false`). Se eliminó el fixture muerto `test_settings` que usaba
kwargs inexistentes.

### ✅ 4.3 — Carpeta `contract/` vacía — HECHO
Eliminada (solo tenía `__init__`).

### ✅ 4.4 — Artefactos de cobertura versionados — HECHO
Añadido `.gitignore` que excluye `coverage.xml`, `htmlcov/`, `.venv/`, `__pycache__/`, `.env`,
`docker_images/`, cachés de ruff/mypy/pytest, etc. (listo para cuando se inicialice git).

---

## 5. TYPING / mypy — ✅ HECHO

`mypy api-service` = **Success, 0 issues** (27 archivos). Los dos avisos se resolvieron con
`# type: ignore` documentados y acotados (`settings = Settings()` y el `params` de httpx).
Pendiente/futuro: endurecer gradualmente (`disallow_untyped_defs = true`) módulo a módulo.

---

## 6. MANTENIBILIDAD / ESTRUCTURA

### ⏸️ M1 — ~150 endpoints son boilerplate idéntico — NO HECHO (deliberado)
Reescribir las firmas de ~150 endpoints es churn puro sin ganancia funcional y con riesgo de
regresión. **Decisión: no tocar ahora.** Se puede centralizar la auth con `Depends` más
adelante si se busca mejor doc OpenAPI; no es un bug.

### ✅ M2 — `requirements.txt` duplicado — HECHO
Eliminado `api-service/requirements.txt` (el Dockerfile usa el de la raíz, confirmado por el
contexto de build). Fuente única: `requirements.txt` raíz + `pyproject.toml`.

### ✅ M3 — Versión inconsistente — HECHO
Unificada a `1.2026.8` en `Settings.app_version`, ambos `ARG APP_VERSION` del Dockerfile y
`pyproject.toml`.

### M4 — Constantes globales en `proxy.py`
`BASE_URL`, `API_KEY`, etc. se leen a nivel de módulo desde `settings`. Funciona, pero mezcla
config global mutable con la instancia `Settings`. Menor; considerar acceder siempre vía
`settings.` para testeo más fácil.

---

## 7. SEGURIDAD (revisión ligera)

- ✅ **HECHO** — Auth por API key con **`secrets.compare_digest`** (comparación en tiempo
  constante, evita timing attacks).
- ✅ **HECHO** — **CORS** vía `CORSMiddleware`, orígenes acotados por `CORS_ALLOW_ORIGINS`
  (vacío por defecto = sin acceso cross-origin; nunca `*`). Verificado funcionalmente.
- ✅ Docker con usuario no-root, multi-stage. Bien.
- 🟡 La API key va en header (bien); documentar que **no** debe ir en query string.
- 🟡 El endpoint `/health` expone `version` y detalle de error del upstream. Aceptable en
  interno; si es público, considerar reducir el detalle. (No es website-facing, bajo riesgo.)

---

## 7b. Ronda de revisión externa (2026-07-16) — aplicado

Segundo deep review independiente. Dispiciones:

**Aplicado:**
- **P1 · Passthrough de bytes** — respuestas no-JSON/XML (CSV, binario, otros charsets) ahora
  se reenvían con `upstream.content` **verbatim** (antes `text.encode("utf-8")` podía corromper
  contenido no transformado). Test: `test_resilience.py::test_non_json_body_is_forwarded_verbatim`.
- **P1 · `/live` vs `/health`** — nuevo `/live` (liveness local, no toca upstream); el
  healthcheck de Docker/Compose apunta a `/live`. Así una caída/rate-limit/DNS del upstream no
  marca el contenedor unhealthy mientras el proxy sirve (incluso desde caché). `/health` queda
  como readiness. Verificado: `docker inspect` → `healthy`.
- **P2 · Cache key sin colisiones** — `_cache_key` usa `urlencode(sorted(params))`; `?a=1&b=2`
  y `?a=1%26b=2` ya no colapsan a la misma entrada. Tests en `test_proxy_transform.py`.
- **P2 · Smoke tests** — ahora se **saltan por defecto** (hook `pytest_collection_modifyitems`
  + opción `--run-smoke`); ya no inflan la corrida normal (294 pasan, 15 smoke skipped).
- **P3 · Docs configurables** — `ENABLE_DOCS` (default `true`) apaga `/docs`, `/redoc`,
  `/openapi.json` para prod público.
- **P3 · Docs desactualizadas** — `api-service/README.md` reescrito (refleja ~150 rutas +
  resiliencia/caché); `PORTAINER_DEPLOYMENT.md` actualizado a `1.2026.10`.

**No aplicado (con criterio):**
- **P2 · Tests placeholder** — quitar los `pass` es cosmético; no agrega cobertura real. El core
  de errores está cubierto; los routers son wrappers idénticos ya ejercitados.
- **P2 · Python 3.14 (test) vs 3.12 (prod)** — es proceso, no código; ya construimos y probamos
  la imagen en Docker (3.12). Se podría añadir un target "test-in-docker".
- **P3 · Upper bounds de dependencias** — el artefacto reproducible es el tar de la imagen; poner
  bounds "a ojo" puede causar más problemas. Si se quiere reproducibilidad estricta → lockfile.

---

## 8. PREPARACIÓN PARA ETAPA 2 (Statcast / Baseball Savant)

La arquitectura actual asume **un solo upstream** (`BASE_URL`) y **dos formatos** (XML/JSON).
Baseball Savant:
- Usa otro dominio (`baseballsavant.mlb.com`).
- Sirve **CSV** en varios endpoints (`/statcast_search/csv`), formato no soportado hoy.
- Devuelve datasets grandes y lentos.

**Implicaciones (refuerzan la Etapa 1):**
1. Generalizar `forward_get` para soportar **múltiples upstreams** (o un cliente httpx dedicado
   a Savant, ver R1).
2. Añadir **manejo de CSV** (parseo a JSON o passthrough con streaming).
3. **Caché** (R3) pasa de "deseable" a "necesario" por el peso de las consultas.
4. Considerar **streaming** de respuestas grandes en vez de cargar todo en memoria
   (`upstream.text` actual lee todo el body).

---

## 9. PLAN SUGERIDO (orden de ataque)

**Bloque 1 — Resiliencia núcleo (mayor ROI):**
1. R1 · Cliente httpx compartido con pool + `lifespan`.
2. R5 · Timeouts granulares (connect vs total).
3. R2 · Reintentos con backoff.
4. R6 · `/health` reutiliza el cliente compartido.

**Bloque 2 — Correctitud de datos:**
5. C2 · Decidir contrato de traducción (opt-in) + alinear test 4.1.
6. C1 · Acotar `normalize_null_values` a campos de stats.
7. 4.2 · Limpiar `conftest.py`.

**Bloque 3 — Escala y exposición (pre-website):**
8. R3 · Caché con TTL por tipo de endpoint.
9. R4 · Rate limiting.
10. CORS + `secrets.compare_digest`.

**Bloque 4 — Base para Statcast:**
11. Multi-upstream + soporte CSV + streaming.

**Transversal (ya iniciado):** ruff/mypy en el flujo de trabajo; limpiar estilo en `test/`;
consolidar dependencias y versión; inicializar git cuando quieras para rastrear todo esto.
```
