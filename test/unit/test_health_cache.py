"""El sondeo de `/health` a la API de MLB, y por qué se reutiliza unos segundos.

QUÉ PROTEGE ESTO
----------------
Antes, CADA llamada a `/health` salía a la API de MLB. El healthcheck del contenedor corre cada 30
segundos por su cuenta —2.880 peticiones diarias— y cualquier monitor externo añade las suyas
encima, todo para contestar una pregunta cuya respuesta no cambia de un segundo a otro. Bajo un
límite de tasa, comprobar la salud competiría con el tráfico de verdad.
"""

import asyncio
from typing import Any

import pytest


class _Respuesta:
    def __init__(self, codigo: int) -> None:
        self.status_code = codigo


class _ClienteContador:
    """Cuenta cuántas veces se sale de verdad a MLB."""

    def __init__(self, codigo: int = 200) -> None:
        self.llamadas = 0
        self._codigo = codigo

    async def get(self, url: str, timeout: float = 0) -> _Respuesta:
        self.llamadas += 1
        return _Respuesta(self._codigo)


class _Peticion:
    def __init__(self, cliente: Any) -> None:
        self.app = type("App", (), {"state": type("Estado", (), {"http": cliente})()})()


@pytest.fixture(autouse=True)
def _sin_memoria() -> Any:
    """Cada prueba empieza con el sondeo olvidado: si no, la primera contamina a las demás."""
    import main

    main._UPSTREAM_PROBE = None
    yield
    main._UPSTREAM_PROBE = None


def test_dentro_del_ttl_no_se_vuelve_a_salir_a_mlb() -> None:
    """Diez comprobaciones seguidas tienen que costar UNA petición a MLB, no diez."""
    import main

    main.settings.health_upstream_ttl = 30.0
    cliente = _ClienteContador()
    peticion = _Peticion(cliente)

    for _ in range(10):
        asyncio.run(main._probe_upstream(peticion))

    assert cliente.llamadas == 1


def test_con_el_ttl_en_cero_se_sale_siempre() -> None:
    """La vía de escape: `HEALTH_UPSTREAM_TTL=0` devuelve el comportamiento de antes."""
    import main

    main.settings.health_upstream_ttl = 0.0
    cliente = _ClienteContador()
    peticion = _Peticion(cliente)

    for _ in range(3):
        asyncio.run(main._probe_upstream(peticion))

    assert cliente.llamadas == 3


def test_el_fallo_tambien_se_recuerda() -> None:
    """A propósito, y es cuando más importa: durante una caída cada sondeo cuesta 5 segundos de
    espera, así que repetirlo en cada comprobación es justo lo que no se quiere."""
    import main

    main.settings.health_upstream_ttl = 30.0
    cliente = _ClienteContador(codigo=503)
    peticion = _Peticion(cliente)

    primero = asyncio.run(main._probe_upstream(peticion))
    segundo = asyncio.run(main._probe_upstream(peticion))

    assert primero == segundo
    assert primero[0] is False
    assert cliente.llamadas == 1


def test_pasado_el_ttl_se_vuelve_a_preguntar() -> None:
    """Una recuperación se reporta dentro de un TTL. Se envejece el sondeo en vez de esperar de
    verdad: una prueba que duerme treinta segundos es una prueba que nadie corre."""
    import main

    main.settings.health_upstream_ttl = 30.0
    cliente = _ClienteContador()
    peticion = _Peticion(cliente)

    asyncio.run(main._probe_upstream(peticion))
    envejecido, sano, error = main._UPSTREAM_PROBE
    main._UPSTREAM_PROBE = (envejecido - 31.0, sano, error)
    asyncio.run(main._probe_upstream(peticion))

    assert cliente.llamadas == 2
