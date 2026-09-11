"""
Testes para o Agente de Regras de Negócio e Elegibilidade.
"""

import pytest
from src.agents.business_rules_agent import BusinessRulesAgent
from src.models import (
    AlertaRisco,
    TipoAmeaca,
    SeveridadeRisco,
    Apolice,
    TipoRamo
)


def test_carregamento_base_segurados():
    agent = BusinessRulesAgent()
    assert len(agent.segurados) > 0


def test_filtragem_por_cidade():
    agent = BusinessRulesAgent()
    sp_segurados = agent.filtrar_segurados_por_localizacao("São Paulo")
    assert len(sp_segurados) > 0
    assert any("São Paulo" in s.cidade for s in sp_segurados)


def test_elegibilidade_apolice_granizo_auto():
    agent = BusinessRulesAgent()
    apolice_auto = Apolice(
        id="APO-TEST-1",
        tipo_ramo=TipoRamo.AUTO,
        descricao_bem="Sedan 2024",
        coberturas=["Colisão", "Granizo"],
        valor_assegurado_reais=100000.0
    )
    alerta_granizo = AlertaRisco(
        id="ALERTA-01",
        tipo_ameaca=TipoAmeaca.GRANIZO,
        severidade=SeveridadeRisco.ALTO,
        descricao_motivo="Granizo iminente",
        limiar_atingido="75%",
        cidade="Curitiba",
        estado="PR",
        data_evento="2026-08-22",
        probabilidade_ocorrencia_pct=75.0
    )
    assert agent.verificar_elegibilidade_apolice(apolice_auto, alerta_granizo) is True
