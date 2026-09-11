"""
Orquestrador do Fluxo Multiagente (Workflow Orchestrator).
Coordena a execução em esteira de todos os agentes especializados:
1. Agente Coletor Meteorológico
2. Agente Analisador de Risco Climático
3. Agente de Regras de Negócio de Seguros
4. Agente de Comunicação Proativa com IA
5. Agente Simulador de Envio e Auditoria
"""

import time
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.agents.collector_agent import WeatherCollectorAgent
from src.agents.risk_agent import ClimateRiskAgent
from src.agents.business_rules_agent import BusinessRulesAgent
from src.agents.communication_agent import CommunicationAgent
from src.agents.dispatcher_agent import DispatcherAgent
from src.models import (
    EventoClimatico,
    AlertaRisco,
    Notificacao,
    MetricasPipeline,
    RespostaAgente
)

logger = logging.getLogger(__name__)


class RegistroPassoExecucao(BaseModel):
    passo: int
    nome_agente: str
    papel: str
    status: str
    detalhes: str
    tempo_ms: float
    dados_saida: Dict[str, Any] = Field(default_factory=dict)


class ResultadoExecucaoPipeline(BaseModel):
    id_execucao: str
    modo_origem: str  # 'cenario' ou 'tempo_real'
    evento_climatico: EventoClimatico
    alertas_identificados: List[AlertaRisco] = Field(default_factory=list)
    notificacoes_geradas: List[Notificacao] = Field(default_factory=list)
    metricas: MetricasPipeline
    rastros_agentes: List[RegistroPassoExecucao] = Field(default_factory=list)
    sucesso: bool = True
    mensagem_status: str = "Pipeline concluído com sucesso."


class PipelineOrchestrator:
    """Orquestrador central do pipeline multiagente de comunicação preventiva."""

    def __init__(
        self,
        collector: Optional[WeatherCollectorAgent] = None,
        risk_agent: Optional[ClimateRiskAgent] = None,
        rules_agent: Optional[BusinessRulesAgent] = None,
        comm_agent: Optional[CommunicationAgent] = None,
        dispatcher: Optional[DispatcherAgent] = None,
    ):
        self.collector = collector or WeatherCollectorAgent()
        self.risk_agent = risk_agent or ClimateRiskAgent()
        self.rules_agent = rules_agent or BusinessRulesAgent()
        self.comm_agent = comm_agent or CommunicationAgent()
        self.dispatcher = dispatcher or DispatcherAgent()

    def executar_pipeline(
        self,
        modo: str = "cenario",
        identificador: str = "CENARIO-01"
    ) -> ResultadoExecucaoPipeline:
        """
        Executa todas as 5 etapas da solução com observabilidade e rastreabilidade total.
        """
        inicio_total = time.time()
        rastros: List[RegistroPassoExecucao] = []
        execucao_id = f"EXEC-{int(time.time())}"

        # ----------------------------------------------------
        # ETAPA 1: Coleta de Dados Meteorológicos
        # ----------------------------------------------------
        t0 = time.time()
        evento: EventoClimatico = self.collector.executar(modo=modo, identificador=identificador)
        dt1 = (time.time() - t0) * 1000
        rastros.append(RegistroPassoExecucao(
            passo=1,
            nome_agente=self.collector.nome,
            papel=self.collector.papel,
            status="CONCLUÍDO",
            detalhes=f"Dados obtidos para {evento.cidade}-{evento.estado}: Precipitação {evento.precipitacao_mm}mm, Rajada {evento.rajada_vento_kmh}km/h, Condição '{evento.descricao_condicao}'.",
            tempo_ms=round(dt1, 2),
            dados_saida={"evento": evento.model_dump()}
        ))

        # ----------------------------------------------------
        # ETAPA 2: Identificação de Riscos Climáticos
        # ----------------------------------------------------
        t0 = time.time()
        alertas: List[AlertaRisco] = self.risk_agent.executar(evento)
        dt2 = (time.time() - t0) * 1000
        resumo_alertas = f"{len(alertas)} alerta(s) de risco identificado(s)." if alertas else "Clima seguro. Nenhum alerta crítico gerado."
        rastros.append(RegistroPassoExecucao(
            passo=2,
            nome_agente=self.risk_agent.nome,
            papel=self.risk_agent.papel,
            status="CONCLUÍDO",
            detalhes=resumo_alertas,
            tempo_ms=round(dt2, 2),
            dados_saida={"total_alertas": len(alertas), "alertas": [a.model_dump() for a in alertas]}
        ))

        # Se não houver alertas, encerra precocemente com status seguro
        if not alertas:
            tempo_total = time.time() - inicio_total
            metricas = self.dispatcher.calcular_metricas(
                total_avaliados=len(self.rules_agent.segurados),
                notificacoes=[],
                tempo_total=tempo_total
            )
            return ResultadoExecucaoPipeline(
                id_execucao=execucao_id,
                modo_origem=modo,
                evento_climatico=evento,
                alertas_identificados=[],
                notificacoes_geradas=[],
                metricas=metricas,
                rastros_agentes=rastros,
                sucesso=True,
                mensagem_status="Condições climáticas normais. Nenhuma comunicação preventiva necessária."
            )

        # ----------------------------------------------------
        # ETAPA 3: Aplicação de Regras de Negócio e Elegibilidade
        # ----------------------------------------------------
        t0 = time.time()
        destinatarios = self.rules_agent.executar(alertas)
        dt3 = (time.time() - t0) * 1000
        rastros.append(RegistroPassoExecucao(
            passo=3,
            nome_agente=self.rules_agent.nome,
            papel=self.rules_agent.papel,
            status="CONCLUÍDO",
            detalhes=f"Base analisada ({len(self.rules_agent.segurados)} segurados). {len(destinatarios)} apólice(s) elegível(is) para notificação preventiva.",
            tempo_ms=round(dt3, 2),
            dados_saida={"total_elegiveis": len(destinatarios)}
        ))

        # ----------------------------------------------------
        # ETAPA 4: Geração Automática das Mensagens com IA
        # ----------------------------------------------------
        t0 = time.time()
        notificacoes_brutas: List[Notificacao] = self.comm_agent.executar(destinatarios)
        dt4 = (time.time() - t0) * 1000
        rastros.append(RegistroPassoExecucao(
            passo=4,
            nome_agente=self.comm_agent.nome,
            papel=self.comm_agent.papel,
            status="CONCLUÍDO",
            detalhes=f"{len(notificacoes_brutas)} mensagem(ns) personalizadas e empáticas redigidas com inteligência generativa.",
            tempo_ms=round(dt4, 2),
            dados_saida={"total_mensagens": len(notificacoes_brutas)}
        ))

        # ----------------------------------------------------
        # ETAPA 5: Simulação de Envio e Telemetria Multicanal
        # ----------------------------------------------------
        t0 = time.time()
        notificacoes_enviadas: List[Notificacao] = self.dispatcher.executar(notificacoes_brutas)
        dt5 = (time.time() - t0) * 1000
        rastros.append(RegistroPassoExecucao(
            passo=5,
            nome_agente=self.dispatcher.nome,
            papel=self.dispatcher.papel,
            status="CONCLUÍDO",
            detalhes=f"{len(notificacoes_enviadas)} disparo(s) simulados com sucesso em múltiplos canais (WhatsApp, SMS, Push, E-mail).",
            tempo_ms=round(dt5, 2),
            dados_saida={"total_despachadas": len(notificacoes_enviadas)}
        ))

        # Consolidação de Métricas Finais
        tempo_total = time.time() - inicio_total
        metricas = self.dispatcher.calcular_metricas(
            total_avaliados=len(self.rules_agent.segurados),
            notificacoes=notificacoes_enviadas,
            tempo_total=tempo_total
        )

        return ResultadoExecucaoPipeline(
            id_execucao=execucao_id,
            modo_origem=modo,
            evento_climatico=evento,
            alertas_identificados=alertas,
            notificacoes_geradas=notificacoes_enviadas,
            metricas=metricas,
            rastros_agentes=rastros,
            sucesso=True,
            mensagem_status="Pipeline multiagente executado com êxito total."
        )
