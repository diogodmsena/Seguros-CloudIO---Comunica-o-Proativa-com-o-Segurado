"""
Testes de Integração Ponta a Ponta do Pipeline Multiagente.
"""

import pytest
from src.agents.orchestrator import PipelineOrchestrator


def test_execucao_pipeline_cenario_tempestade_sp():
    orchestrator = PipelineOrchestrator()
    resultado = orchestrator.executar_pipeline(modo="cenario", identificador="CENARIO-01")
    
    assert resultado.sucesso is True
    assert len(resultado.alertas_identificados) > 0
    assert len(resultado.notificacoes_geradas) > 0
    assert len(resultado.rastros_agentes) == 5  # Todos os 5 agentes executaram
    assert resultado.metricas.total_notificacoes_geradas > 0
    assert resultado.metricas.economia_sinistros_estimada_reais > 0


def test_execucao_pipeline_cenario_granizo_curitiba():
    orchestrator = PipelineOrchestrator()
    resultado = orchestrator.executar_pipeline(modo="cenario", identificador="CENARIO-02")
    
    assert resultado.sucesso is True
    assert any("Granizo" in a.tipo_ameaca.value for a in resultado.alertas_identificados)
    assert any(n.ramo.value == "Auto" for n in resultado.notificacoes_geradas)


def test_execucao_pipeline_tempo_bom_sem_disparos():
    orchestrator = PipelineOrchestrator()
    resultado = orchestrator.executar_pipeline(modo="cenario", identificador="CENARIO-06")
    
    assert resultado.sucesso is True
    assert len(resultado.alertas_identificados) == 0
    assert len(resultado.notificacoes_geradas) == 0
