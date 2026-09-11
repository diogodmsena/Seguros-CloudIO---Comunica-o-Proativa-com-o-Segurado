"""
Classe Base para Agentes Especializados.
Fornece infraestrutura comum de logging, medição de tempo e rastreabilidade didática.
"""

import time
import logging
from typing import Dict, Any
from abc import ABC, abstractmethod
from src.models import RespostaAgente

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Classe base abstrata para todos os agentes inteligentes do pipeline."""

    def __init__(self, nome: str, papel: str, objetivo: str):
        self.nome = nome
        self.papel = papel
        self.objetivo = objetivo
        self.logger = logging.getLogger(f"Agente.{self.__class__.__name__}")

    def registrar_passo(self, mensagem: str):
        """Registra um log informativo didático com o nome do agente."""
        self.logger.info(f"[{self.nome}] {mensagem}")

    @abstractmethod
    def executar(self, *args, **kwargs) -> Any:
        """Método principal a ser implementado por cada agente especializado."""
        pass

    def executar_com_rastreamento(self, func_execucao, *args, **kwargs) -> tuple[Any, RespostaAgente]:
        """Executa a lógica do agente medindo tempo e gerando metadados estruturados."""
        inicio = time.time()
        self.registrar_passo(f"Iniciando tarefa: {self.objetivo}")
        try:
            resultado = func_execucao(*args, **kwargs)
            tempo_ms = (time.time() - inicio) * 1000
            self.registrar_passo(f"Tarefa concluída com sucesso em {tempo_ms:.2f}ms.")
            resposta = RespostaAgente(
                nome_agente=self.nome,
                status="SUCESSO",
                resumo_execucao=f"Execução finalizada com êxito em {tempo_ms:.1f} ms.",
                tempo_execucao_ms=tempo_ms
            )
            return resultado, resposta
        except Exception as e:
            tempo_ms = (time.time() - inicio) * 1000
            self.logger.error(f"[{self.nome}] Erro durante execução: {e}", exc_info=True)
            resposta = RespostaAgente(
                nome_agente=self.nome,
                status="ERRO",
                resumo_execucao=f"Falha na execução: {str(e)}",
                tempo_execucao_ms=tempo_ms
            )
            raise e
