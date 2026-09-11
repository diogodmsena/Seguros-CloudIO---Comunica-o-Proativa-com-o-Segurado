"""
Testes para o Agente de Análise de Risco Climático.
"""

import pytest
from src.agents.risk_agent import ClimateRiskAgent
from src.models import EventoClimatico, TipoAmeaca, SeveridadeRisco


def test_analise_risco_chuva_intensa():
    agent = ClimateRiskAgent()
    evento = EventoClimatico(
        cidade="São Paulo",
        estado="SP",
        latitude=-23.55,
        longitude=-46.63,
        temperatura_c=22.0,
        sensacao_c=22.0,
        precipitacao_mm=65.0,  # Alta precipitação
        probabilidade_chuva_pct=95.0,
        velocidade_vento_kmh=20.0,
        rajada_vento_kmh=40.0,
        probabilidade_granizo_pct=10.0,
        descricao_condicao="Chuva forte com trovoada",
        fonte_dados="Teste"
    )
    alertas = agent.analisar_evento(evento)
    assert len(alertas) >= 1
    alerta_chuva = next((a for a in alertas if a.tipo_ameaca == TipoAmeaca.CHUVA_INTENSA), None)
    assert alerta_chuva is not None
    assert alerta_chuva.severidade in [SeveridadeRisco.ALTO, SeveridadeRisco.CRITICO]


def test_analise_risco_granizo():
    agent = ClimateRiskAgent()
    evento = EventoClimatico(
        cidade="Curitiba",
        estado="PR",
        latitude=-25.42,
        longitude=-49.27,
        temperatura_c=18.0,
        sensacao_c=17.0,
        precipitacao_mm=30.0,
        probabilidade_chuva_pct=85.0,
        velocidade_vento_kmh=35.0,
        rajada_vento_kmh=50.0,
        probabilidade_granizo_pct=85.0,  # Granizo crítico
        descricao_condicao="Tempestade severa com granizo",
        fonte_dados="Teste"
    )
    alertas = agent.analisar_evento(evento)
    alerta_granizo = next((a for a in alertas if a.tipo_ameaca == TipoAmeaca.GRANIZO), None)
    assert alerta_granizo is not None
    assert alerta_granizo.severidade == SeveridadeRisco.CRITICO


def test_analise_tempo_bom_sem_alertas():
    agent = ClimateRiskAgent()
    evento = EventoClimatico(
        cidade="Belo Horizonte",
        estado="MG",
        latitude=-19.91,
        longitude=-43.93,
        temperatura_c=25.0,
        sensacao_c=25.0,
        precipitacao_mm=0.0,
        probabilidade_chuva_pct=5.0,
        velocidade_vento_kmh=10.0,
        rajada_vento_kmh=15.0,
        probabilidade_granizo_pct=0.0,
        descricao_condicao="Céu limpo",
        fonte_dados="Teste"
    )
    alertas = agent.analisar_evento(evento)
    assert len(alertas) == 0
