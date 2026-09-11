"""
Serviço de Coleta e Integração de Dados Meteorológicos.
Conecta-se à API pública global Open-Meteo (sem necessidade de chaves de API)
e oferece suporte a cenários simulados e geocodificação de cidades.
"""

import json
import logging
from typing import Dict, Any, Optional, List
import requests

from src.config import (
    WEATHER_API_URL,
    WEATHER_GEOCODING_URL,
    REQUEST_TIMEOUT,
    CIDADES_PADRAO,
    CENARIOS_FILE
)
from src.models import EventoClimatico

logger = logging.getLogger(__name__)

# Tabela de Códigos Meteorológicos WMO (World Meteorological Organization)
WMO_WEATHER_CODES = {
    0: "Céu limpo / Ensolarado",
    1: "Predomínio de sol com poucas nuvens",
    2: "Parcialmente nublado",
    3: "Nublado / Encoberto",
    45: "Nevoeiro / Neblina densa",
    48: "Nevoeiro com depósito de gelo",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa densa",
    56: "Garoa congelante leve",
    57: "Garoa congelante densa",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte / intensa",
    66: "Chuva congelante leve",
    67: "Chuva congelante forte",
    71: "Queda de neve leve",
    73: "Queda de neve moderada",
    75: "Queda de neve forte",
    77: "Grãos de gelo / sincelo",
    80: "Pancadas de chuva fracas",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva violentas / torrenciais",
    85: "Pancadas de neve fracas",
    86: "Pancadas de neve fortes",
    95: "Tempestade com trovoadas",
    96: "Tempestade com granizo leve/moderado",
    99: "Tempestade severa com queda violenta de granizo",
}


class WeatherService:
    """Serviço para obter dados climáticos via Open-Meteo ou cenários pré-configurados."""

    def __init__(self):
        self._cenarios_cache: Optional[List[Dict[str, Any]]] = None

    def carregar_cenarios_simulados(self) -> List[Dict[str, Any]]:
        """Carrega a lista de cenários pré-configurados para testes didáticos."""
        if self._cenarios_cache is None:
            if CENARIOS_FILE.exists():
                with open(CENARIOS_FILE, "r", encoding="utf-8") as f:
                    self._cenarios_cache = json.load(f)
            else:
                self._cenarios_cache = []
        return self._cenarios_cache

    def obter_cenario_por_id(self, cenario_id: str) -> Optional[EventoClimatico]:
        """Obtém um evento climático a partir de um ID de cenário simulado."""
        cenarios = self.carregar_cenarios_simulados()
        for c in cenarios:
            if c.get("id") == cenario_id:
                return EventoClimatico(
                    cidade=c["cidade"],
                    estado=c["estado"],
                    latitude=c["latitude"],
                    longitude=c["longitude"],
                    temperatura_c=c["temperatura_c"],
                    sensacao_c=c["sensacao_c"],
                    precipitacao_mm=c["precipitacao_mm"],
                    probabilidade_chuva_pct=c["probabilidade_chuva_pct"],
                    velocidade_vento_kmh=c["velocidade_vento_kmh"],
                    rajada_vento_kmh=c["rajada_vento_kmh"],
                    probabilidade_granizo_pct=c.get("probabilidade_granizo_pct", 0.0),
                    descricao_condicao=c["descricao_condicao"],
                    fonte_dados=c.get("fonte_dados", "Cenário Simulado Didático")
                )
        return None

    def buscar_coordenadas_cidade(self, nome_cidade: str) -> Optional[Dict[str, Any]]:
        """
        Busca latitude e longitude de uma cidade brasileira.
        Primeiro verifica nas cidades padrão; se não encontrar, usa a API de geocodificação.
        """
        # Checa cidades padrão
        for cidade_key, dados in CIDADES_PADRAO.items():
            if nome_cidade.lower() in cidade_key.lower():
                partes = cidade_key.split(" - ")
                return {
                    "cidade": partes[0],
                    "estado": partes[1] if len(partes) > 1 else "",
                    "lat": dados["lat"],
                    "lon": dados["lon"]
                }

        # Consulta Geocoding API pública
        try:
            params = {
                "name": nome_cidade,
                "count": 1,
                "language": "pt",
                "format": "json"
            }
            resp = requests.get(WEATHER_GEOCODING_URL, params=params, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    first = results[0]
                    return {
                        "cidade": first.get("name", nome_cidade),
                        "estado": first.get("admin1", ""),
                        "lat": first.get("latitude"),
                        "lon": first.get("longitude")
                    }
        except Exception as e:
            logger.warning(f"Erro ao geocodificar cidade {nome_cidade}: {e}")

        return None

    def consultar_clima_tempo_real(self, latitude: float, longitude: float, cidade: str = "", estado: str = "") -> EventoClimatico:
        """
        Consulta a API pública Open-Meteo para obter as condições climáticas e previsão horária.
        Calcula probabilidades de granizo e rajadas de vento baseadas nos códigos meteorológicos e variáveis atmosféricas.
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "rain",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_gusts_10m"
                ],
                "hourly": [
                    "precipitation_probability",
                    "precipitation",
                    "wind_gusts_10m"
                ],
                "timezone": "America/Sao_Paulo",
                "forecast_days": 1
            }

            response = requests.get(WEATHER_API_URL, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})
            hourly = data.get("hourly", {})

            temp = current.get("temperature_2m", 20.0)
            sensacao = current.get("apparent_temperature", temp)
            precip = current.get("precipitation", 0.0)
            vento_kmh = current.get("wind_speed_10m", 10.0)
            rajada_kmh = current.get("wind_gusts_10m", vento_kmh * 1.3)
            weather_code = current.get("weather_code", 0)

            # Probabilidade máxima de chuva nas próximas horas
            prob_chuva_list = hourly.get("precipitation_probability", [0])
            prob_chuva = max(prob_chuva_list[:12]) if prob_chuva_list else 0.0

            # Estima probabilidade de granizo com base no código meteorológico WMO
            if weather_code == 99:
                prob_granizo = 90.0
            elif weather_code == 96:
                prob_granizo = 65.0
            elif weather_code == 95:
                prob_granizo = 35.0
            else:
                prob_granizo = 5.0 if precip > 30.0 else 0.0

            descricao = WMO_WEATHER_CODES.get(weather_code, f"Condição climática (Código WMO {weather_code})")

            return EventoClimatico(
                cidade=cidade or "Localização Consultada",
                estado=estado or "",
                latitude=latitude,
                longitude=longitude,
                temperatura_c=temp,
                sensacao_c=sensacao,
                precipitacao_mm=precip,
                probabilidade_chuva_pct=float(prob_chuva),
                velocidade_vento_kmh=vento_kmh,
                rajada_vento_kmh=rajada_kmh,
                probabilidade_granizo_pct=prob_granizo,
                descricao_condicao=descricao,
                fonte_dados="Open-Meteo API (Tempo Real)"
            )

        except Exception as e:
            logger.error(f"Erro na consulta à API Open-Meteo: {e}. Utilizando dados de fallback.")
            # Fallback robusto para quando estiver sem conexão com a internet
            return EventoClimatico(
                cidade=cidade or "São Paulo",
                estado=estado or "SP",
                latitude=latitude,
                longitude=longitude,
                temperatura_c=22.0,
                sensacao_c=22.5,
                precipitacao_mm=45.0,
                probabilidade_chuva_pct=80.0,
                velocidade_vento_kmh=28.0,
                rajada_vento_kmh=55.0,
                probabilidade_granizo_pct=30.0,
                descricao_condicao="Pancadas de chuva com trovoadas (Modo Resiliente Fallback)",
                fonte_dados="Open-Meteo Fallback Didático"
            )
