"""
Agente 2: Analisador de Riscos Climáticos (Climate Risk Analyzer Agent).
Responsável por analisar os dados meteorológicos, comparar com os limiares técnicos
e identificar se há eventos de risco iminente para a população e segurados.
"""

from typing import List, Optional
import uuid
from src.agents.base_agent import BaseAgent
from src.config import LIMIARES_RISCO
from src.models import EventoClimatico, AlertaRisco, TipoAmeaca, SeveridadeRisco


class ClimateRiskAgent(BaseAgent):
    """Agente especialista na análise e classificação de severidade de eventos meteorológicos."""

    def __init__(self):
        super().__init__(
            nome="Agente de Análise de Risco Climático",
            papel="Meteorologista Especialista em Riscos Naturais",
            objetivo="Identificar anomalias climáticas, calcular severidade e gerar alertas baseados em limiares técnicos."
        )

    def analisar_evento(self, evento: EventoClimatico) -> List[AlertaRisco]:
        """
        Analisa as variáveis meteorológicas do evento e emite a lista de alertas correspondentes.
        Verifica chuva, granizo, vento, frio extremo e tempestades.
        """
        alertas: List[AlertaRisco] = []
        self.registrar_passo(f"Iniciando auditoria de riscos para {evento.cidade} - {evento.estado}...")

        # 1. Avaliação de Granizo
        if evento.probabilidade_granizo_pct >= LIMIARES_RISCO["granizo_probabilidade"]["baixo"]:
            prob = evento.probabilidade_granizo_pct
            if prob >= LIMIARES_RISCO["granizo_probabilidade"]["critico"]:
                sev = SeveridadeRisco.CRITICO
            elif prob >= LIMIARES_RISCO["granizo_probabilidade"]["alto"]:
                sev = SeveridadeRisco.ALTO
            elif prob >= LIMIARES_RISCO["granizo_probabilidade"]["medio"]:
                sev = SeveridadeRisco.MEDIO
            else:
                sev = SeveridadeRisco.BAIXO

            motivo = (
                f"Probabilidade de {prob:.1f}% de tempestade com granizo, com potencial de danos severos "
                f"a latarias de veículos, telhados, estufas e lavouras agrícolas."
            )
            alertas.append(AlertaRisco(
                id=f"RISK-HAIL-{uuid.uuid4().hex[:6].upper()}",
                tipo_ameaca=TipoAmeaca.GRANIZO,
                severidade=sev,
                descricao_motivo=motivo,
                limiar_atingido=f"Probabilidade de Granizo = {prob:.1f}% (Nível {sev.value})",
                cidade=evento.cidade,
                estado=evento.estado,
                data_evento=evento.data_hora,
                probabilidade_ocorrencia_pct=prob,
                acoes_recomendadas=[
                    "Abrigar veículos em garagens cobertas imediatamente.",
                    "Proteger estufas e hortifrutigranjeiros com telas antigranizo.",
                    "Evitar transitar a pé ou de carro em áreas abertas durante a chuva de pedras."
                ]
            ))
            self.registrar_passo(f"⚠️ Alerta identificado: {TipoAmeaca.GRANIZO.value} - Severidade: {sev.value}")

        # 2. Avaliação de Chuva Intensa / Alagamento
        if evento.precipitacao_mm >= LIMIARES_RISCO["chuva_intensa"]["baixo"] or (evento.probabilidade_chuva_pct >= 80 and evento.precipitacao_mm >= 20):
            precip = evento.precipitacao_mm
            if precip >= LIMIARES_RISCO["chuva_intensa"]["critico"]:
                sev = SeveridadeRisco.CRITICO
            elif precip >= LIMIARES_RISCO["chuva_intensa"]["alto"]:
                sev = SeveridadeRisco.ALTO
            elif precip >= LIMIARES_RISCO["chuva_intensa"]["medio"]:
                sev = SeveridadeRisco.MEDIO
            else:
                sev = SeveridadeRisco.BAIXO

            motivo = (
                f"Precipitação intensa acumulada/horária estimada em {precip:.1f} mm/h (Probabilidade de {evento.probabilidade_chuva_pct:.0f}%), "
                f"elevando drasticamente o risco de enxurradas, pontos de alagamento urbano e deslizamentos."
            )
            alertas.append(AlertaRisco(
                id=f"RISK-RAIN-{uuid.uuid4().hex[:6].upper()}",
                tipo_ameaca=TipoAmeaca.CHUVA_INTENSA,
                severidade=sev,
                descricao_motivo=motivo,
                limiar_atingido=f"Precipitação = {precip:.1f} mm/h (Nível {sev.value})",
                cidade=evento.cidade,
                estado=evento.estado,
                data_evento=evento.data_hora,
                probabilidade_ocorrencia_pct=evento.probabilidade_chuva_pct,
                acoes_recomendadas=[
                    "Desobstruir calhas, ralos e grelhas residenciais e industriais.",
                    "Elevar móveis, eletrodomésticos e estoques do chão em áreas sujeitas a inundação.",
                    "Evitar transitar por vias alagadas ou sob pontilhões."
                ]
            ))
            self.registrar_passo(f"⚠️ Alerta identificado: {TipoAmeaca.CHUVA_INTENSA.value} - Severidade: {sev.value}")

        # 3. Avaliação de Rajadas de Vento / Vendaval
        max_vento = max(evento.velocidade_vento_kmh, evento.rajada_vento_kmh)
        if max_vento >= LIMIARES_RISCO["vento_forte"]["baixo"]:
            if max_vento >= LIMIARES_RISCO["vento_forte"]["critico"]:
                sev = SeveridadeRisco.CRITICO
            elif max_vento >= LIMIARES_RISCO["vento_forte"]["alto"]:
                sev = SeveridadeRisco.ALTO
            elif max_vento >= LIMIARES_RISCO["vento_forte"]["medio"]:
                sev = SeveridadeRisco.MEDIO
            else:
                sev = SeveridadeRisco.BAIXO

            motivo = (
                f"Rajadas de vento registradas/previstas de até {max_vento:.1f} km/h, com risco iminente de destelhamento, "
                f"queda de galhos/árvores sobre veículos e imóveis, e interrupção na rede elétrica."
            )
            alertas.append(AlertaRisco(
                id=f"RISK-WIND-{uuid.uuid4().hex[:6].upper()}",
                tipo_ameaca=TipoAmeaca.VENDAVAL,
                severidade=sev,
                descricao_motivo=motivo,
                limiar_atingido=f"Rajada de Vento = {max_vento:.1f} km/h (Nível {sev.value})",
                cidade=evento.cidade,
                estado=evento.estado,
                data_evento=evento.data_hora,
                probabilidade_ocorrencia_pct=85.0,
                acoes_recomendadas=[
                    "Recolher objetos soltos em sacadas, varandas e quintais.",
                    "Não estacionar veículos debaixo de árvores ou perto de postes e outdoors.",
                    "Fechar e travar portas, portões e janelas."
                ]
            ))
            self.registrar_passo(f"⚠️ Alerta identificado: {TipoAmeaca.VENDAVAL.value} - Severidade: {sev.value}")

        # 4. Avaliação de Geada / Frio Extremo
        if evento.temperatura_c <= LIMIARES_RISCO["frio_extremo"]["baixo"]:
            temp = evento.temperatura_c
            if temp <= LIMIARES_RISCO["frio_extremo"]["critico"]:
                sev = SeveridadeRisco.CRITICO
            elif temp <= LIMIARES_RISCO["frio_extremo"]["alto"]:
                sev = SeveridadeRisco.ALTO
            elif temp <= LIMIARES_RISCO["frio_extremo"]["medio"]:
                sev = SeveridadeRisco.MEDIO
            else:
                sev = SeveridadeRisco.BAIXO

            motivo = (
                f"Queda brusca de temperatura para {temp:.1f}°C (Sensação térmica de {evento.sensacao_c:.1f}°C), "
                f"com formação de geada severa, risco de queima foliar em lavouras e danos a encanamentos."
            )
            alertas.append(AlertaRisco(
                id=f"RISK-FROST-{uuid.uuid4().hex[:6].upper()}",
                tipo_ameaca=TipoAmeaca.GEADA,
                severidade=sev,
                descricao_motivo=motivo,
                limiar_atingido=f"Temperatura Mínima = {temp:.1f}°C (Nível {sev.value})",
                cidade=evento.cidade,
                estado=evento.estado,
                data_evento=evento.data_hora,
                probabilidade_ocorrencia_pct=90.0,
                acoes_recomendadas=[
                    "Cobrir lavouras e canteiros agrícolas sensíveis com palha ou lona protetora.",
                    "Abrigar animais de criação e maquinários agrícolas em locais aquecidos e fechados.",
                    "Isolar tubulações externas de água contra congelamento."
                ]
            ))
            self.registrar_passo(f"⚠️ Alerta identificado: {TipoAmeaca.GEADA.value} - Severidade: {sev.value}")

        if not alertas:
            self.registrar_passo(f"Condições climáticas estáveis para {evento.cidade}. Nenhum limiar crítico atingido.")

        return alertas

    def executar(self, evento: EventoClimatico) -> List[AlertaRisco]:
        """Executa a análise de risco para o evento climático fornecido."""
        return self.analisar_evento(evento)
