"""
Agente 3: Especialista em Regras de Negócio de Seguros (Insurance Business Rules Agent).
Responsável por cruzar os alertas meteorológicos com a base de segurados,
identificar bens expostos e determinar quais apólices devem receber comunicações.
"""

import json
import logging
from typing import List, Dict, Any, Tuple, Optional
from src.agents.base_agent import BaseAgent
from src.config import SEGURADOS_FILE
from src.models import (
    Segurado,
    Apolice,
    AlertaRisco,
    TipoRamo,
    TipoAmeaca,
    CanalNotificacao,
    SeveridadeRisco
)

logger = logging.getLogger(__name__)


# Matriz de Vulnerabilidade: Quais ramos de seguro são vulneráveis a quais tipos de ameaça climática
MATRIZ_VULNERABILIDADE = {
    TipoAmeaca.GRANIZO: [TipoRamo.AUTO, TipoRamo.RESIDENCIAL, TipoRamo.AGRO, TipoRamo.EMPRESARIAL],
    TipoAmeaca.CHUVA_INTENSA: [TipoRamo.AUTO, TipoRamo.RESIDENCIAL, TipoRamo.EMPRESARIAL, TipoRamo.AGRO],
    TipoAmeaca.VENDAVAL: [TipoRamo.RESIDENCIAL, TipoRamo.EMPRESARIAL, TipoRamo.AUTO, TipoRamo.AGRO],
    TipoAmeaca.GEADA: [TipoRamo.AGRO, TipoRamo.RESIDENCIAL],
    TipoAmeaca.TEMPESTADE_ELETRICA: [TipoRamo.RESIDENCIAL, TipoRamo.EMPRESARIAL, TipoRamo.AGRO],
    TipoAmeaca.ONDA_CALOR_SECA: [TipoRamo.AGRO, TipoRamo.VIDA]
}


class BusinessRulesAgent(BaseAgent):
    """Agente especialista em regras de negócio securitárias e segmentação de carteira."""

    def __init__(self, lista_segurados: Optional[List[Segurado]] = None):
        super().__init__(
            nome="Agente de Regras de Negócio de Seguros",
            papel="Subscritor e Especialista em Apólices e Gestão de Carteira",
            objetivo="Cruzar dados geográficos e contratuais para identificar segurados elegíveis para comunicação preventiva."
        )
        self.segurados = lista_segurados or self.carregar_segurados_do_arquivo()

    def carregar_segurados_do_arquivo(self) -> List[Segurado]:
        """Carrega a base didática de segurados do arquivo JSON."""
        if not SEGURADOS_FILE.exists():
            self.logger.warning(f"Arquivo {SEGURADOS_FILE} não encontrado.")
            return []
        try:
            with open(SEGURADOS_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return [Segurado(**item) for item in dados]
        except Exception as e:
            self.logger.error(f"Erro ao carregar segurados: {e}")
            return []

    def filtrar_segurados_por_localizacao(self, cidade: str, estado: str = "") -> List[Segurado]:
        """Filtra segurados que residem ou possuem patrimônio na cidade/região afetada."""
        cidade_norm = cidade.strip().lower()
        estado_norm = estado.strip().lower()

        selecionados = []
        for s in self.segurados:
            if cidade_norm in s.cidade.lower() or s.cidade.lower() in cidade_norm:
                if not estado_norm or estado_norm == s.estado.lower():
                    selecionados.append(s)
        return selecionados

    def verificar_elegibilidade_apolice(self, apolice: Apolice, alerta: AlertaRisco) -> bool:
        """
        Verifica se a apólice possui relevância para o tipo de alerta climático.
        1. Verifica se o ramo é vulnerável à ameaça.
        2. Verifica se a apólice cobre o evento ou se o bem tem risco físico direto.
        """
        ramos_vulneraveis = MATRIZ_VULNERABILIDADE.get(alerta.tipo_ameaca, [])
        if apolice.tipo_ramo not in ramos_vulneraveis:
            return False

        # Verifica se o nível de severidade justifica disparo de notificação
        # Notificações são acionadas para níveis Médio, Alto e Crítico (ou Baixo se for Agro/Granizo)
        if alerta.severidade == SeveridadeRisco.BAIXO and apolice.tipo_ramo != TipoRamo.AGRO:
            return False

        return True

    def selecionar_canal_otimizado(self, segurado: Segurado, alerta: AlertaRisco) -> CanalNotificacao:
        """
        Determina o melhor canal de envio.
        Para alertas Críticos com urgência imediata, prioriza WhatsApp ou SMS caso configurado.
        """
        if alerta.severidade == SeveridadeRisco.CRITICO:
            # Em risco crítico, WhatsApp tem a maior taxa de abertura em tempo hábil
            return CanalNotificacao.WHATSAPP
        return segurado.canal_preferencial

    def processar_regras(self, alertas: List[AlertaRisco]) -> List[Tuple[Segurado, Apolice, AlertaRisco, CanalNotificacao]]:
        """
        Aplica todas as regras de negócio para uma lista de alertas climáticos.
        Retorna a lista de tuplas (Segurado, Apolice, Alerta, Canal) prontas para a redação.
        """
        destinatarios: List[Tuple[Segurado, Apolice, AlertaRisco, CanalNotificacao]] = []
        self.registrar_passo(f"Avaliando base de {len(self.segurados)} segurados cadastrados contra {len(alertas)} alerta(s)...")

        for alerta in alertas:
            candidatos = self.filtrar_segurados_por_localizacao(alerta.cidade, alerta.estado)
            self.registrar_passo(f"Alerta '{alerta.tipo_ameaca.value}' em {alerta.cidade}: {len(candidatos)} segurados na região.")

            for segurado in candidatos:
                for apolice in segurado.apolices:
                    if self.verificar_elegibilidade_apolice(apolice, alerta):
                        canal = self.selecionar_canal_otimizado(segurado, alerta)
                        destinatarios.append((segurado, apolice, alerta, canal))
                        self.registrar_passo(
                            f"-> Aprovado para notificação: {segurado.nome} (Apólice: {apolice.id} - {apolice.tipo_ramo.value} / {apolice.descricao_bem}) via {canal.value}."
                        )

        self.registrar_passo(f"Total de {len(destinatarios)} comunicações aprovadas pelas regras de negócio.")
        return destinatarios

    def executar(self, alertas: List[AlertaRisco]) -> List[Tuple[Segurado, Apolice, AlertaRisco, CanalNotificacao]]:
        """Executa o processamento completo de regras de negócio."""
        return self.processar_regras(alertas)
