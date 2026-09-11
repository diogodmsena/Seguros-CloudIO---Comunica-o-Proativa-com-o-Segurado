"""
Módulo de Configuração Geral do Sistema.
Gerencia variáveis de ambiente, caminhos de arquivos e limiares de regras de negócio.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env caso exista
load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = SRC_DIR / "data"

# Arquivos de dados
SEGURADOS_FILE = DATA_DIR / "segurados.json"
CENARIOS_FILE = DATA_DIR / "cenarios_climaticos.json"
RELATORIO_MD = BASE_DIR / "relatorio_tecnico.md"
RELATORIO_PDF = BASE_DIR / "relatorio_tecnico.pdf"

# Chaves de API para Modelos de Linguagem (opcionais, com fallback didático automático)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto")  # 'gemini', 'openai', 'local' ou 'auto'

# Configurações de Clima e API Pública
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REQUEST_TIMEOUT = 10  # segundos

# Cidades Brasileiras Mapeadas (Coordenadas padrão para demonstração rápida)
CIDADES_PADRAO = {
    "São Paulo - SP": {"lat": -23.5505, "lon": -46.6333, "estado": "SP"},
    "Curitiba - PR": {"lat": -25.4284, "lon": -49.2733, "estado": "PR"},
    "Rio de Janeiro - RJ": {"lat": -22.9068, "lon": -43.1729, "estado": "RJ"},
    "Porto Alegre - RS": {"lat": -30.0346, "lon": -51.2177, "estado": "RS"},
    "Belo Horizonte - MG": {"lat": -19.9167, "lon": -43.9345, "estado": "MG"},
    "Salvador - BA": {"lat": -12.9777, "lon": -38.5016, "estado": "BA"},
    "Recife - PE": {"lat": -8.0476, "lon": -34.8770, "estado": "PE"},
    "Florianópolis - SC": {"lat": -27.5954, "lon": -48.5480, "estado": "SC"},
    "Campinas - SP": {"lat": -22.9056, "lon": -47.0608, "estado": "SP"},
    "Ribeirão Preto - SP": {"lat": -21.1704, "lon": -47.8103, "estado": "SP"},
}

# Limiares de Risco Meteorológico (Baseados em referências da Defesa Civil / INMET)
LIMIARES_RISCO = {
    # Precipitação em mm/h ou acumulado em 24h
    "chuva_intensa": {
        "baixo": 15.0,    # mm/h
        "medio": 30.0,
        "alto": 50.0,
        "critico": 80.0
    },
    # Rajadas de Vento em km/h
    "vento_forte": {
        "baixo": 45.0,    # km/h
        "medio": 60.0,
        "alto": 75.0,
        "critico": 90.0
    },
    # Granizo (probabilidade em %)
    "granizo_probabilidade": {
        "baixo": 20.0,    # %
        "medio": 45.0,
        "alto": 70.0,
        "critico": 85.0
    },
    # Frio Extremo / Geada (Temperatura mínima em °C)
    "frio_extremo": {
        "baixo": 8.0,     # °C
        "medio": 4.0,
        "alto": 1.0,
        "critico": -2.0
    }
}
