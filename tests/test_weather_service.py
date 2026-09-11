"""
Testes para o WeatherService e Coleta de Dados Meteorológicos.
"""

import pytest
from src.services.weather_service import WeatherService
from src.models import EventoClimatico


def test_carregar_cenarios():
    service = WeatherService()
    cenarios = service.carregar_cenarios_simulados()
    assert len(cenarios) > 0
    assert any(c["id"] == "CENARIO-01" for c in cenarios)


def test_obter_cenario_por_id():
    service = WeatherService()
    evento = service.obter_cenario_por_id("CENARIO-01")
    assert evento is not None
    assert isinstance(evento, EventoClimatico)
    assert evento.cidade == "São Paulo"
    assert evento.precipitacao_mm > 50


def test_buscar_coordenadas_cidade_padrao():
    service = WeatherService()
    geo = service.buscar_coordenadas_cidade("Curitiba")
    assert geo is not None
    assert "lat" in geo
    assert "lon" in geo
    assert geo["lat"] < -20  # Hemisfério sul


def test_fallback_resiliente_open_meteo():
    service = WeatherService()
    # Coordenadas válidas para consulta
    evento = service.consultar_clima_tempo_real(latitude=-23.5505, longitude=-46.6333, cidade="São Paulo", estado="SP")
    assert isinstance(evento, EventoClimatico)
    assert evento.cidade == "São Paulo"
    assert evento.temperatura_c is not None
