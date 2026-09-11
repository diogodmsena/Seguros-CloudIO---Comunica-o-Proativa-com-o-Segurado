"""
Agente 4: Comunicador Proativo com IA Generativa (Proactive Communication Agent / Copywriter).
Responsável por orquestrar a IA Generativa (Gemini, OpenAI ou Motor Local)
para redigir mensagens empáticas, altamente personalizadas e acionáveis.
"""

import uuid
from typing import List, Tuple, Optional
from src.agents.base_agent import BaseAgent
from src.services.llm_service import LLMService
from src.models import (
    Segurado,
    Apolice,
    AlertaRisco,
    CanalNotificacao,
    Notificacao
)


class CommunicationAgent(BaseAgent):
    """Agente especialista em redação de mensagens preventivas com IA Generativa."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        super().__init__(
            nome="Agente de Comunicação Proativa com IA",
            papel="Redator Empático e Especialista em IA Generativa de Riscos",
            objetivo="Gerar mensagens personalizadas, didáticas e empáticas com orientações práticas para os segurados."
        )
        self.llm_service = llm_service or LLMService()

    def gerar_notificacao_individual(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> Notificacao:
        """Invoca o serviço de IA para redigir a notificação individual."""
        self.registrar_passo(
            f"Gerando comunicação via IA para {segurado.nome} (Apólice: {apolice.descricao_bem}, Canal: {canal.value})..."
        )
        conteudo = self.llm_service.gerar_comunicacao_preventiva(
            segurado=segurado,
            apolice=apolice,
            alerta=alerta,
            canal=canal
        )

        notificacao = Notificacao(
            id=f"NOTIF-{uuid.uuid4().hex[:8].upper()}",
            segurado_id=segurado.id,
            segurado_nome=segurado.nome,
            segurado_telefone=segurado.telefone,
            segurado_email=segurado.email,
            cidade=segurado.cidade,
            apolice_id=apolice.id,
            ramo=apolice.tipo_ramo,
            bem_assegurado=apolice.descricao_bem,
            canal=canal,
            severidade=alerta.severidade,
            titulo=conteudo.get("titulo", f"Alerta Preventivo: {alerta.tipo_ameaca.value}"),
            mensagem_texto=conteudo.get("mensagem_texto", ""),
            orientacoes_seguranca=conteudo.get("orientacoes_seguranca", []),
            custo_sinistro_evitado_estimado_reais=conteudo.get("custo_sinistro_evitado_estimado_reais", 0.0),
            status_envio="Pronto para Disparo"
        )
        return notificacao

    def processar_lote_comunicacoes(
        self,
        destinatarios: List[Tuple[Segurado, Apolice, AlertaRisco, CanalNotificacao]]
    ) -> List[Notificacao]:
        """Gera as notificações em lote para todos os segurados elegíveis."""
        notificacoes: List[Notificacao] = []
        self.registrar_passo(f"Iniciando ciclo de geração generativa para {len(destinatarios)} destinatário(s)...")

        for segurado, apolice, alerta, canal in destinatarios:
            notif = self.gerar_notificacao_individual(segurado, apolice, alerta, canal)
            notificacoes.append(notif)

        self.registrar_passo(f"Geração de comunicações finalizada: {len(notificacoes)} mensagens produzidas.")
        return notificacoes

    def executar(
        self,
        destinatarios: List[Tuple[Segurado, Apolice, AlertaRisco, CanalNotificacao]]
    ) -> List[Notificacao]:
        """Executa a redação em lote das mensagens."""
        return self.processar_lote_comunicacoes(destinatarios)
