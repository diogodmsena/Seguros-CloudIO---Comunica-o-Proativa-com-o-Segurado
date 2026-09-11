"""
Serviço de Inteligência Artificial Generativa para Redação Proativa de Mensagens.
Suporta Google Gemini, OpenAI e um Motor Generativo Didático Local Embutido (Zero-Setup).
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from src.config import GEMINI_API_KEY, OPENAI_API_KEY, LLM_PROVIDER
from src.models import Segurado, Apolice, AlertaRisco, TipoRamo, SeveridadeRisco, CanalNotificacao

logger = logging.getLogger(__name__)


class LLMService:
    """Gerenciador de Modelos de Linguagem para Comunicação Proativa com o Segurado."""

    def __init__(self):
        self.provider = LLM_PROVIDER.lower()
        self.gemini_client = None
        self.openai_client = None
        self._inicializar_provedores()

    def _inicializar_provedores(self):
        """Tenta inicializar os clientes das APIs disponíveis."""
        # Tenta Gemini
        if GEMINI_API_KEY:
            try:
                # Tenta google.genai novo ou google.generativeai legado
                try:
                    from google import genai
                    self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
                    logger.info("Cliente Google GenAI inicializado com sucesso.")
                except ImportError:
                    import google.generativeai as gai
                    gai.configure(api_key=GEMINI_API_KEY)
                    self.gemini_client = gai.GenerativeModel('gemini-1.5-flash')
                    logger.info("Cliente Google GenerativeAI (legado) inicializado.")
            except Exception as e:
                logger.warning(f"Não foi possível inicializar o cliente Gemini: {e}")

        # Tenta OpenAI
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
                logger.info("Cliente OpenAI inicializado com sucesso.")
            except Exception as e:
                logger.warning(f"Não foi possível inicializar o cliente OpenAI: {e}")

    def gerar_comunicacao_preventiva(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> Dict[str, Any]:
        """
        Gera uma comunicação personalizada e empática com orientações de segurança.
        Seleciona automaticamente o provedor configurado ou usa o motor didático local.
        """
        # Se houver cliente Gemini disponível e não for forçado local
        if self.gemini_client and self.provider in ["auto", "gemini"]:
            resultado = self._gerar_com_gemini(segurado, apolice, alerta, canal)
            if resultado:
                return resultado

        # Se houver cliente OpenAI disponível
        if self.openai_client and self.provider in ["auto", "openai"]:
            resultado = self._gerar_com_openai(segurado, apolice, alerta, canal)
            if resultado:
                return resultado

        # Motor Didático Local (Execução local garantida, rápida e sem necessidade de chave)
        return self._gerar_com_motor_didatico(segurado, apolice, alerta, canal)

    def _construir_prompt_sistema(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> str:
        """Gera o prompt estruturado com todas as variáveis de contexto."""
        return f"""Você é o Agente Especialista em Comunicação Proativa e Prevenção de Riscos da Seguradora Seguros CloudIO.
Sua missão é redigir uma mensagem empática, clara, proativa e altamente didática para alertar o segurado sobre um risco climático iminente e orientá-lo a proteger seu patrimônio e sua família ANTES que o sinistro ocorra.

DADOS DO SEGURADO E APÓLICE:
- Nome: {segurado.nome}
- Cidade/Estado: {segurado.cidade}/{segurado.estado} (Bairro: {segurado.bairro})
- Ramo: {apolice.tipo_ramo.value}
- Bem Assegurado: {apolice.descricao_bem}
- Coberturas da Apólice: {', '.join(apolice.coberturas)}
- Franquia: R$ {apolice.franquia_reais:,.2f}
- Valor Segurado: R$ {apolice.valor_assegurado_reais:,.2f}
- Canal de Envio: {canal.value}

DADOS DO ALERTA CLIMÁTICO:
- Tipo de Ameaça: {alerta.tipo_ameaca.value}
- Severidade: {alerta.severidade.value}
- Motivo Técnico: {alerta.descricao_motivo}
- Probabilidade: {alerta.probabilidade_ocorrencia_pct}%

DIRETRIZES DE COMUNICAÇÃO:
1. Tom: Empático, acolhedor, profissional e urgente (sem causar pânico).
2. Formato por Canal:
   - Se WhatsApp: Use emojis elegantes, quebras de linha claras, negrito para destaque e checklist visual.
   - Se SMS: Muito direto e conciso, com foco na ação imediata.
   - Se Push: Título curto chamativo + corpo objetivo.
   - Se E-mail: Saudação formal, contexto meteorológico detalhado, checklist completo e canais de emergência 24h.
3. Orientações Preventivas: Forneça de 3 a 5 ações práticas e específicas para o bem assegurado ({apolice.descricao_bem}).

Retorne APENAS um JSON válido no formato:
{{
  "titulo": "Título curto do alerta",
  "mensagem_texto": "Corpo completo da mensagem formatada para o canal",
  "orientacoes_seguranca": ["Ação 1", "Ação 2", "Ação 3"],
  "custo_sinistro_evitado_estimado_reais": 5000.00
}}"""

    def _gerar_com_gemini(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> Optional[Dict[str, Any]]:
        """Gera a mensagem utilizando a API do Google Gemini."""
        prompt = self._construir_prompt_sistema(segurado, apolice, alerta, canal)
        try:
            # Novo SDK google.genai
            if hasattr(self.gemini_client, "models"):
                resp = self.gemini_client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                texto = resp.text
            else:
                # SDK legado
                resp = self.gemini_client.generate_content(prompt)
                texto = resp.text

            # Limpa formatação markdown de código json
            texto = texto.strip()
            if texto.startswith("```json"):
                texto = texto[7:]
            if texto.startswith("```"):
                texto = texto[3:]
            if texto.endswith("```"):
                texto = texto[:-3]
            return json.loads(texto.strip())
        except Exception as e:
            logger.warning(f"Falha na geração via Gemini ({e}). Usando motor didático local.")
            return None

    def _gerar_com_openai(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> Optional[Dict[str, Any]]:
        """Gera a mensagem utilizando a API da OpenAI."""
        prompt = self._construir_prompt_sistema(segurado, apolice, alerta, canal)
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente de IA especialista em seguros e prevenção de sinistros."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.warning(f"Falha na geração via OpenAI ({e}). Usando motor didático local.")
            return None

    def _gerar_com_motor_didatico(
        self,
        segurado: Segurado,
        apolice: Apolice,
        alerta: AlertaRisco,
        canal: CanalNotificacao
    ) -> Dict[str, Any]:
        """
        Motor Generativo Didático Embutido:
        Produz mensagens humanas, personalizadas e tecnicamente ricas para qualquer
        combinação de ramo, apólice e evento meteorológico sem depender de chaves de API.
        """
        primeiro_nome = segurado.nome.split()[0]
        severidade = alerta.severidade.value
        tipo_ameaca = alerta.tipo_ameaca.value
        bem = apolice.descricao_bem
        cidade = segurado.cidade

        # Estimativa de custo evitado baseado no ramo e severidade
        fator_custo = {"Baixo": 0.02, "Médio": 0.05, "Alto": 0.12, "Crítico": 0.25}
        pct = fator_custo.get(severidade, 0.05)
        custo_evitado = round(apolice.valor_assegurado_reais * pct, 2)

        # Regras de conteúdo preventivo por Ramo e Ameaça
        orientacoes = []
        if apolice.tipo_ramo == TipoRamo.AUTO:
            if "Granizo" in tipo_ameaca:
                orientacoes = [
                    f"Estacione o seu {bem} em garagem coberta ou estacionamento subterrâneo nas próximas horas.",
                    "Evite estacionar sob árvores com galhos secos ou postes de fiação exposta.",
                    "Se for surpreendido na via, reduza a velocidade e procure abrigo sob pontes ou postos de combustível com segurança.",
                    "Mantenha o aplicativo da seguradora atualizado para acionamento de guincho 24h caso necessário."
                ]
            elif "Chuva" in tipo_ameaca or "Alagamento" in tipo_ameaca:
                orientacoes = [
                    f"Evite trafegar por vias com histórico de alagamento conhecidas em {cidade}.",
                    "Nunca tente atravessar enxurradas se a água ultrapassar a metade da roda do veículo.",
                    "Prefira rotas elevadas e reduza a velocidade devido ao risco de aquaplanagem.",
                    "Se o carro morrer na água, não dê a partida novamente para evitar calço hidráulico no motor."
                ]
            else:
                orientacoes = [
                    f"Mantenha o seu {bem} em local seguro, longe de árvores e painéis publicitários.",
                    "Verifique os limpadores de para-brisa e as condições dos pneus.",
                    "Dirija com faróis baixos acesos e dobre a distância de segurança do veículo à frente."
                ]

        elif apolice.tipo_ramo == TipoRamo.RESIDENCIAL:
            if "Chuva" in tipo_ameaca or "Alagamento" in tipo_ameaca:
                orientacoes = [
                    "Verifique e desobstrua calhas, ralos e grelhas de escoamento do imóvel.",
                    "Desconecte aparelhos eletrônicos sensíveis da tomada para evitar queima por descargas na rede.",
                    "Coloque móveis e documentos importantes em locais elevados caso more em área rebaixada.",
                    "Feche bem janelas, portas e claraboias antes do início da tempestade."
                ]
            elif "Vendaval" in tipo_ameaca:
                orientacoes = [
                    "Recolha ou amarre objetos soltos em quintais, varandas e áreas externas (mesas, vasos, lonas).",
                    "Inspecione telhas soltas e certifique-se de que janelas estejam bem travadas.",
                    "Evite permanecer próximo a janelas de vidro de grandes dimensões durante as rajadas mais fortes.",
                    "Tenha lanternas a pilha à mão caso ocorra interrupção no fornecimento de energia elétrica."
                ]
            else:
                orientacoes = [
                    "Desconecte eletrodomésticos das tomadas durante a tempestade de raios.",
                    "Verifique a integridade do telhado e calhas de drenagem.",
                    "Mantenha os números de emergência (Defesa Civil 199 e Seguradora) salvos no celular."
                ]

        elif apolice.tipo_ramo == TipoRamo.AGRO:
            if "Geada" in tipo_ameaca or "Frio" in tipo_ameaca:
                orientacoes = [
                    "Acione sistemas de irrigação por aspersão preventiva (quando aplicável) antes do pico de queda térmica.",
                    "Proteja mudas e culturas sensíveis com cobertura plástica, palhada ou túneis baixos.",
                    "Abrigue maquinários agrícolas e tratores em galpões fechados para evitar congelamento de fluidos.",
                    "Verifique o estoque e fornecimento de água e aquecimento para animais de criação."
                ]
            elif "Granizo" in tipo_ameaca:
                orientacoes = [
                    "Estenda telas antigranizo em pomares e estufas com antecedência.",
                    "Recolha maquinários e implementos agrícolas para áreas cobertas protegidas.",
                    "Monitore os canais de telemetria climática rural da seguradora em tempo real."
                ]
            else:
                orientacoes = [
                    "Reforce a fixação de estruturas de estufas e silos de armazenagem contra ventos fortes.",
                    "Mantenha tratores e veículos agrícolas estacionados em áreas planas e protegidas.",
                    "Revise os canais de drenagem da propriedade rural."
                ]

        elif apolice.tipo_ramo == TipoRamo.EMPRESARIAL:
            orientacoes = [
                f"Inspecione a vedação e telhado do {bem} antes da chegada do evento severo.",
                "Eleve estoques e mercadorias sensíveis a pelo menos 30 cm do nível do piso em depósitos.",
                "Teste geradores de energia de emergência e proteja servidores e CPDs com nobreaks.",
                "Oriente a equipe de brigada e segurança patrimonial sobre os protocolos de evacuação preventiva."
            ]

        else:
            orientacoes = [
                "Permaneça em local seguro e protegido durante a tempestade.",
                "Evite transitar por vias alagadas ou sob árvores e estruturas metálicas.",
                "Mantenha seus familiares e animais de estimação em local protegido."
            ]

        # Adaptação para o canal
        if canal == CanalNotificacao.WHATSAPP:
            titulo = f"⚠️ Alerta Preventivo de Proteção | Seguros CloudIO - {severidade}"
            mensagem = (
                f"Olá, *{primeiro_nome}*! 👋\n\n"
                f"Nossa central de inteligência climática identificou um alerta de *{tipo_ameaca}* com severidade *{severidade.upper()}* para a sua região em *{cidade}*.\n\n"
                f"🛡️ *Patrimônio Protegido:* {bem}\n"
                f"📋 *Apólice:* {apolice.id} ({apolice.tipo_ramo.value})\n"
                f"⛈️ *Condição Prevista:* {alerta.descricao_motivo}\n\n"
                f"Para manter você e seu patrimônio em total segurança, preparamos estas *recomendações preventivas imediatas*:\n\n"
            )
            for idx, item in enumerate(orientacoes, 1):
                mensagem += f"{idx}️⃣ {item}\n"

            mensagem += (
                f"\n💡 *Lembre-se:* Sua apólice está ativa e conta com cobertura para este evento. "
                f"Caso necessite de assistência 24 horas, estamos à disposição pelo 0800-700-SAFE."
            )

        elif canal == CanalNotificacao.SMS:
            titulo = f"ALERTA SEGUROS CLOUDIO: {tipo_ameaca} ({severidade})"
            mensagem = (
                f"Seguros CloudIO Alerta: Risco de {tipo_ameaca} em {cidade}. "
                f"Proteja seu {bem}. Ação: {orientacoes[0]} Dúvidas/Guincho 24h: 0800-700-7233."
            )

        elif canal == CanalNotificacao.PUSH:
            titulo = f"⚠️ Risco de {tipo_ameaca} em {cidade}"
            mensagem = (
                f"{primeiro_nome}, proteja seu {bem}! Severidade: {severidade}. "
                f"{orientacoes[0]}"
            )

        else:  # EMAIL
            titulo = f"Aviso de Segurança Preventiva: Alerta de {tipo_ameaca} em {cidade}"
            mensagem = (
                f"Prezado(a) {segurado.nome},\n\n"
                f"Como parte do nosso compromisso de cuidado contínuo e prevenção com a sua tranquilidade, "
                f"nosso sistema inteligente de monitoramento identificou condições meteorológicas severas "
                f"previstas para a sua localidade em {cidade} - {segurado.estado}.\n\n"
                f"DETALHES DO EVENTO CLIMÁTICO:\n"
                f"• Ameaça: {tipo_ameaca}\n"
                f"• Nível de Severidade: {severidade}\n"
                f"• Detalhamento: {alerta.descricao_motivo}\n"
                f"• Bem Assegurado: {bem} (Apólice Nº {apolice.id})\n\n"
                f"CHECKLIST PREVENTIVO RECOMENDADO:\n"
            )
            for idx, item in enumerate(orientacoes, 1):
                mensagem += f"  [{idx}] {item}\n"

            mensagem += (
                f"\nCaso ocorra qualquer eventualidade, nossa equipe de atendimento e assistência 24 horas "
                f"está pronta para apoiá-lo.\n\n"
                f"Atenciosamente,\n"
                f"Equipe de Prevenção e Atendimento ao Segurado\nSeguros CloudIO Inteligentes"
            )

        return {
            "titulo": titulo,
            "mensagem_texto": mensagem,
            "orientacoes_seguranca": orientacoes,
            "custo_sinistro_evitado_estimado_reais": custo_evitado
        }
