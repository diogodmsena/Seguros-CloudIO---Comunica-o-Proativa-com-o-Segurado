"""
Modelos de Dados do Sistema de Comunicação Proativa.
Utiliza Pydantic para validação, tipagem e serialização consistente.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TipoRamo(str, Enum):
    AUTO = "Auto"
    RESIDENCIAL = "Residencial"
    AGRO = "Agro"
    EMPRESARIAL = "Empresarial"
    VIDA = "Vida"


class SeveridadeRisco(str, Enum):
    BAIXO = "Baixo"
    MEDIO = "Médio"
    ALTO = "Alto"
    CRITICO = "Crítico"


class TipoAmeaca(str, Enum):
    CHUVA_INTENSA = "Chuva Intensa / Alagamento"
    GRANIZO = "Queda de Granizo"
    VENDAVAL = "Vendaval / Ventos Fortes"
    TEMPESTADE_ELETRICA = "Tempestade com Raios"
    GEADA = "Geada / Frio Extremo"
    ONDA_CALOR_SECA = "Onda de Calor / Seca Severa"


class CanalNotificacao(str, Enum):
    WHATSAPP = "WhatsApp"
    SMS = "SMS"
    PUSH = "Push Notification"
    EMAIL = "E-mail"


class Apolice(BaseModel):
    id: str
    tipo_ramo: TipoRamo
    descricao_bem: str  # Ex: "Toyota Corolla 2023", "Residência Sobrado", "Galpão Industrial", "Lavoura de Soja"
    coberturas: List[str]  # Ex: ["Colisão", "Granizo", "Alagamento", "Incêndio", "Vendaval"]
    franquia_reais: float = 0.0
    valor_assegurado_reais: float = 0.0
    vigencia_fim: str = "2027-12-31"


class Segurado(BaseModel):
    id: str
    nome: str
    email: str
    telefone: str
    cidade: str
    estado: str
    bairro: str
    latitude: float
    longitude: float
    canal_preferencial: CanalNotificacao = CanalNotificacao.WHATSAPP
    apolices: List[Apolice] = Field(default_factory=list)


class EventoClimatico(BaseModel):
    cidade: str
    estado: str
    latitude: float
    longitude: float
    data_hora: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    temperatura_c: float
    sensacao_c: float
    precipitacao_mm: float
    probabilidade_chuva_pct: float
    velocidade_vento_kmh: float
    rajada_vento_kmh: float
    probabilidade_granizo_pct: float = 0.0
    descricao_condicao: str
    fonte_dados: str = "Open-Meteo API"


class AlertaRisco(BaseModel):
    id: str
    tipo_ameaca: TipoAmeaca
    severidade: SeveridadeRisco
    descricao_motivo: str
    limiar_atingido: str
    cidade: str
    estado: str
    data_evento: str
    probabilidade_ocorrencia_pct: float
    acoes_recomendadas: List[str] = Field(default_factory=list)


class Notificacao(BaseModel):
    id: str
    segurado_id: str
    segurado_nome: str
    segurado_telefone: str
    segurado_email: str
    cidade: str
    apolice_id: str
    ramo: TipoRamo
    bem_assegurado: str
    canal: CanalNotificacao
    severidade: SeveridadeRisco
    titulo: str
    mensagem_texto: str
    orientacoes_seguranca: List[str]
    custo_sinistro_evitado_estimado_reais: float = 0.0
    data_geracao: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status_envio: str = "Simulado com Sucesso (Entregue)"
    feedback_cliente: Optional[str] = None


class MetricasPipeline(BaseModel):
    total_segurados_avaliados: int = 0
    total_segurados_em_risco: int = 0
    total_notificacoes_geradas: int = 0
    tempo_execucao_segundos: float = 0.0
    valor_patrimonio_protegido_estimado_reais: float = 0.0
    economia_sinistros_estimada_reais: float = 0.0
    distribuicao_canais: Dict[str, int] = Field(default_factory=dict)
    distribuicao_ramos: Dict[str, int] = Field(default_factory=dict)


class RespostaAgente(BaseModel):
    nome_agente: str
    status: str
    resumo_execucao: str
    detalhes: Dict[str, Any] = Field(default_factory=dict)
    tempo_execucao_ms: float = 0.0
