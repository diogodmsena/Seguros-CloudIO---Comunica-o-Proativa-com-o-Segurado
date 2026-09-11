"""
Agente 5: Simulador de Envio e Roteamento Multicanal (Notification & Dispatch Simulator).
Responsável por simular o disparo das notificações nos diferentes canais (WhatsApp, SMS, Push, E-mail),
registrar a auditoria de entrega, feedbacks simulados e calcular métricas de impacto.
"""

import random
from typing import List, Dict
from src.agents.base_agent import BaseAgent
from src.models import (
    Notificacao,
    MetricasPipeline,
    CanalNotificacao
)

# Respostas simuladas realistas de segurados agradecendo a comunicação preventiva
FEEDBACKS_SIMULADOS = [
    "Recebi o aviso a tempo! Consegui colocar o carro na garagem antes do temporal começar.",
    "Muito obrigado pelo alerta! Desconectei a TV e o computador antes da tempestade de raios.",
    "Excelente iniciativa da seguradora! Cobri a horta e guardei o trator no galpão.",
    "Aviso fundamental! Mudei minha rota para não passar pelo túnel que costuma alagar.",
    "Ótimo suporte preventivo! Fechei todas as janelas e calhas da casa a tempo.",
    "Parabéns pelo cuidado com o segurado. Evitou que o telhado sofresse avarias maiores."
]


class DispatcherAgent(BaseAgent):
    """Agente especialista em simulação de entrega de notificações e métricas operacionais."""

    def __init__(self):
        super().__init__(
            nome="Agente Simulador de Envio e Auditoria",
            papel="Orquestrador de Canais e Analista de Telemetria de Mensagens",
            objetivo="Simular o disparo multicanal, verificar status de entrega e consolidar métricas de valor evitado."
        )

    def simular_envio_notificacao(self, notificacao: Notificacao) -> Notificacao:
        """Simula o envio por canal específico com protocolo e feedback de confirmação."""
        canal = notificacao.canal
        self.registrar_passo(
            f"Disparando via [{canal.value}] para {notificacao.segurado_nome} ({notificacao.segurado_telefone if canal != CanalNotificacao.EMAIL else notificacao.segurado_email})..."
        )

        # Atualiza status de envio
        notificacao.status_envio = f"Entregue com Sucesso via {canal.value} (Simulado)"
        notificacao.feedback_cliente = random.choice(FEEDBACKS_SIMULADOS)

        return notificacao

    def despachar_lote(self, notificacoes: List[Notificacao]) -> List[Notificacao]:
        """Dispara todas as notificações e atualiza status."""
        self.registrar_passo(f"Iniciando fila de despacho para {len(notificacoes)} notificação(ões)...")
        enviadas = []
        for n in notificacoes:
            n_atualizada = self.simular_envio_notificacao(n)
            enviadas.append(n_atualizada)
        self.registrar_passo(f"Fila de disparo 100% concluída. Todas as notificações foram simuladas.")
        return enviadas

    def calcular_metricas(
        self,
        total_avaliados: int,
        notificacoes: List[Notificacao],
        tempo_total: float
    ) -> MetricasPipeline:
        """Calcula as métricas de impacto econômico e operacional do pipeline."""
        dist_canais: Dict[str, int] = {}
        dist_ramos: Dict[str, int] = {}
        economia_total = 0.0
        patrimonio_total = 0.0

        for n in notificacoes:
            # Contagem de canais
            dist_canais[n.canal.value] = dist_canais.get(n.canal.value, 0) + 1
            # Contagem de ramos
            dist_ramos[n.ramo.value] = dist_ramos.get(n.ramo.value, 0) + 1
            # Economia de sinistros
            economia_total += n.custo_sinistro_evitado_estimado_reais

        metricas = MetricasPipeline(
            total_segurados_avaliados=total_avaliados,
            total_segurados_em_risco=len(set(n.segurado_id for n in notificacoes)),
            total_notificacoes_geradas=len(notificacoes),
            tempo_execucao_segundos=round(tempo_total, 2),
            valor_patrimonio_protegido_estimado_reais=patrimonio_total,
            economia_sinistros_estimada_reais=round(economia_total, 2),
            distribuicao_canais=dist_canais,
            distribuicao_ramos=dist_ramos
        )
        return metricas

    def executar(self, notificacoes: List[Notificacao]) -> List[Notificacao]:
        """Executa a simulação de disparo em lote."""
        return self.despachar_lote(notificacoes)
