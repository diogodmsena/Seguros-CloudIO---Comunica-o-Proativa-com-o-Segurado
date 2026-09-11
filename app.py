"""
Aplicação Web Interativa - Seguros CloudIO (Desafio 5 - I2A2).
Ferramenta Inteligente para Comunicação Proativa com o Segurado.
Interface didática, moderna e completa construída em Streamlit.
"""

import streamlit as st
import pandas as pd
import json
import time
import os

from src.config import CIDADES_PADRAO, CENARIOS_FILE, SEGURADOS_FILE
from src.agents.orchestrator import PipelineOrchestrator
from src.agents.collector_agent import WeatherCollectorAgent
from src.agents.business_rules_agent import BusinessRulesAgent
from src.models import TipoRamo, CanalNotificacao, SeveridadeRisco

# Configuração da página Streamlit
st.set_page_config(
    page_title="Seguros CloudIO | Comunicação Proativa com o Segurado",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para um design moderno e elegante
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .agent-card {
        background-color: #f8fafc;
        border-left: 5px solid #0284c7;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .risk-badge-critico {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #f87171;
    }
    
    .risk-badge-alto {
        background-color: #ffedd5;
        color: #9a3412;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #fb923c;
    }
    
    .risk-badge-medio {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #facc15;
    }
    
    .risk-badge-baixo {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #4ade80;
    }
    
    .whatsapp-bubble {
        background-color: #dcf8c6;
        color: #075e54;
        padding: 16px;
        border-radius: 12px 12px 0 12px;
        margin: 12px 0;
        border: 1px solid #b2dfdb;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .sms-bubble {
        background-color: #f1f5f9;
        color: #1e293b;
        padding: 14px;
        border-radius: 12px;
        margin: 10px 0;
        border: 1px solid #cbd5e1;
        font-family: monospace;
    }
    
    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_orchestrator():
    return PipelineOrchestrator()


@st.cache_data
def carregar_dados_iniciais():
    collector = WeatherCollectorAgent()
    cenarios = collector.listar_cenarios_disponiveis()
    rules_agent = BusinessRulesAgent()
    segurados = rules_agent.segurados
    return cenarios, segurados


cenarios, segurados = carregar_dados_iniciais()
orchestrator = get_orchestrator()

# Header Superior
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 700;">🛡️ Seguros CloudIO | Comunicação Proativa</h1>
            <p style="margin: 6px 0 0 0; opacity: 0.85; font-size: 1.05rem;">
                Desafio 5 (I2A2) - Inteligência Artificial para Prevenção e Alerta Proativo a Segurados
            </p>
        </div>
        <div style="background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 8px; font-weight: 600;">
            🚀 Protótipo Didático MVP
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navegação por Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ Demonstração do Pipeline Multiagente",
    "📱 Simulador de Notificações nos Canais",
    "👥 Base de Segurados & Apólices",
    "📊 Painel Executivo & Métricas",
    "📚 Guia Didático & Arquitetura"
])

# ==============================================================================
# ABA 1: EXECUÇÃO DO PIPELINE MULTIAGENTE
# ==============================================================================
with tab1:
    col_ctrl, col_view = st.columns([1, 2.2])

    with col_ctrl:
        st.subheader("⚙️ Configuração da Demonstração")
        
        modo_coleta = st.radio(
            "Fonte de Dados Meteorológicos:",
            ["🌦️ Cenários Simulados Didáticos (Recomendado)", "📡 API Open-Meteo em Tempo Real"],
            index=0
        )

        if "Cenários" in modo_coleta:
            opcoes_cenarios = {f"{c['id']} - {c['nome']} ({c['cidade']})": c['id'] for c in cenarios}
            cenario_selecionado = st.selectbox(
                "Selecione um Cenário Climático:",
                list(opcoes_cenarios.keys())
            )
            cenario_id = opcoes_cenarios[cenario_selecionado]
            modo_exec = "cenario"
            id_exec = cenario_id
        else:
            cidade_selecionada = st.selectbox(
                "Selecione ou digite a Cidade:",
                list(CIDADES_PADRAO.keys())
            )
            modo_exec = "tempo_real"
            id_exec = cidade_selecionada.split(" - ")[0]

        st.markdown("---")
        executar_btn = st.button("🚀 Executar Pipeline Multiagente", type="primary", use_container_width=True)

        st.info("💡 **Dica Didática:** Cada agente possui uma responsabilidade única no fluxo: Coleta ➔ Risco ➔ Regras ➔ Redação IA ➔ Despacho.")

    with col_view:
        if executar_btn or "ultimo_resultado" in st.session_state:
            if executar_btn:
                with st.spinner("Orquestrando agentes inteligentes em tempo real..."):
                    resultado = orchestrator.executar_pipeline(modo=modo_exec, identificador=id_exec)
                    st.session_state["ultimo_resultado"] = resultado
            else:
                resultado = st.session_state["ultimo_resultado"]

            # Resumo do Evento Climático
            ev = resultado.evento_climatico
            st.markdown(f"### 📍 Condições Meteorológicas: **{ev.cidade} - {ev.estado}**")
            
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("🌧️ Precipitação", f"{ev.precipitacao_mm:.1f} mm/h", f"Prob. {ev.probabilidade_chuva_pct:.0f}%")
            with m2:
                st.metric("💨 Rajadas de Vento", f"{ev.rajada_vento_kmh:.1f} km/h", f"Vento: {ev.velocidade_vento_kmh:.1f} km/h")
            with m3:
                st.metric("🧊 Risco de Granizo", f"{ev.probabilidade_granizo_pct:.0f}%", "Probabilidade")
            with m4:
                st.metric("🌡️ Temperatura", f"{ev.temperatura_c:.1f}°C", f"Sensação {ev.sensacao_c:.1f}°C")

            st.caption(f"**Fonte de Dados:** {ev.fonte_dados} | **Condição:** {ev.descricao_condicao}")

            st.markdown("---")
            st.markdown("### 🤖 Rastreamento do Raciocínio dos Agentes")

            for rastro in resultado.rastros_agentes:
                with st.expander(f"Passo {rastro.passo}: **{rastro.nome_agente}** ({rastro.papel}) - ⏱️ {rastro.tempo_ms:.1f}ms", expanded=True):
                    st.markdown(f"**Status:** `{rastro.status}` | **Resultado:** {rastro.detalhes}")
                    if rastro.passo == 2 and resultado.alertas_identificados:
                        for alerta in resultado.alertas_identificados:
                            badge_class = f"risk-badge-{alerta.severidade.value.lower()}"
                            st.markdown(f"<span class='{badge_class}'>⚠️ {alerta.tipo_ameaca.value} ({alerta.severidade.value})</span> — {alerta.descricao_motivo}", unsafe_allow_html=True)

            # Sumário de Notificações
            st.markdown("---")
            st.markdown(f"### 📬 Resultado do Envio: **{len(resultado.notificacoes_geradas)} Notificação(ões) Gerada(s)**")

            if not resultado.notificacoes_geradas:
                st.success("✅ Nenhuma notificação necessária para este cenário climático (condições seguras ou sem ativos expostos).")
            else:
                for notif in resultado.notificacoes_geradas:
                    with st.container():
                        st.markdown(f"""
                        <div class="agent-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4 style="margin: 0; color: #0f172a;">👤 {notif.segurado_nome} ({notif.cidade})</h4>
                                    <p style="margin: 4px 0; color: #64748b; font-size: 0.9rem;">
                                        Apólice <b>{notif.apolice_id}</b> | Ramo <b>{notif.ramo.value}</b> ({notif.bem_assegurado})
                                    </p>
                                </div>
                                <div>
                                    <span class="risk-badge-{notif.severidade.value.lower()}">{notif.severidade.value}</span>
                                    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; margin-left: 6px;">
                                        {notif.canal.value}
                                    </span>
                                </div>
                            </div>
                            <div style="margin-top: 10px; background: white; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                <p style="margin: 0; white-space: pre-line; font-size: 0.95rem; color: #334155;">{notif.mensagem_texto}</p>
                            </div>
                            <div style="margin-top: 8px; font-size: 0.85rem; color: #059669; font-weight: 500;">
                                💬 <b>Feedback Simulado do Segurado:</b> "{notif.feedback_cliente}"
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("👈 Selecione um cenário meteorológico ou cidade e clique no botão **'Executar Pipeline Multiagente'** para iniciar a demonstração.")

# ==============================================================================
# ABA 2: SIMULADOR DE NOTIFICAÇÕES (SMARTPHONE VIEW)
# ==============================================================================
with tab2:
    st.subheader("📱 Simulador de Experiência do Segurado nos Canais de Notificação")
    st.markdown("Veja exatamente como o cliente final recebe a mensagem preventiva no WhatsApp, SMS, Notificação Push ou E-mail.")

    if "ultimo_resultado" in st.session_state and st.session_state["ultimo_resultado"].notificacoes_geradas:
        notificacoes = st.session_state["ultimo_resultado"].notificacoes_geradas
        
        col_list, col_phone = st.columns([1, 1.4])
        
        with col_list:
            nomes_opcoes = [f"{n.segurado_nome} - {n.ramo.value} ({n.canal.value})" for n in notificacoes]
            idx_selecionado = st.selectbox("Selecione o Segurado para Visualização:", range(len(nomes_opcoes)), format_func=lambda x: nomes_opcoes[x])
            notif_selecionada = notificacoes[idx_selecionado]
            
            st.markdown(f"**Segurado:** {notif_selecionada.segurado_nome}")
            st.markdown(f"**Telefone:** {notif_selecionada.segurado_telefone}")
            st.markdown(f"**E-mail:** {notif_selecionada.segurado_email}")
            st.markdown(f"**Localização:** {notif_selecionada.cidade}")
            st.markdown(f"**Bem Assegurado:** {notif_selecionada.bem_assegurado}")
            st.markdown(f"**Economia Estimada em Sinistro:** `R$ {notif_selecionada.custo_sinistro_evitado_estimado_reais:,.2f}`")
            
            st.markdown("#### 📋 Checklist de Ações Preventivas:")
            for acao in notif_selecionada.orientacoes_seguranca:
                st.markdown(f"- ✅ {acao}")

        with col_phone:
            st.markdown(f"### Visualização: **{notif_selecionada.canal.value}**")
            
            if notif_selecionada.canal == CanalNotificacao.WHATSAPP:
                st.markdown(f"""
                <div style="max-width: 450px; background: #efeae2; border-radius: 20px; padding: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); border: 2px solid #cbd5e1;">
                    <div style="background: #075e54; color: white; padding: 10px 14px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.4rem;">🛡️</span>
                        <div>
                            <div style="font-weight: 700; font-size: 0.95rem;">Seguros CloudIO 24h</div>
                            <div style="font-size: 0.75rem; opacity: 0.85;">Conta Comercial Verificada ✔️</div>
                        </div>
                    </div>
                    <div class="whatsapp-bubble">
                        <div style="white-space: pre-line; font-size: 0.9rem; line-height: 1.4;">{notif_selecionada.mensagem_texto}</div>
                        <div style="text-align: right; font-size: 0.7rem; color: #667781; margin-top: 6px;">{time.strftime("%H:%M")} ✔️✔️</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif notif_selecionada.canal == CanalNotificacao.SMS:
                st.markdown(f"""
                <div style="max-width: 450px; background: white; border-radius: 20px; padding: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); border: 2px solid #cbd5e1;">
                    <div style="background: #2563eb; color: white; padding: 10px 14px; border-radius: 12px; margin-bottom: 12px; font-weight: 600;">
                        💬 Mensagem SMS
                    </div>
                    <div class="sms-bubble">
                        {notif_selecionada.mensagem_texto}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif notif_selecionada.canal == CanalNotificacao.PUSH:
                st.markdown(f"""
                <div style="max-width: 450px; background: #1e293b; color: white; border-radius: 20px; padding: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.25);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <span style="font-size: 1.2rem;">🛡️</span>
                        <span style="font-weight: 600; font-size: 0.85rem; color: #94a3b8;">APP SEGUROS CLOUDIO • AGORA</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1rem; margin-bottom: 6px; color: #f8fafc;">
                        {notif_selecionada.titulo}
                    </div>
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.4;">
                        {notif_selecionada.mensagem_texto}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:  # EMAIL
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 20px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <div style="border-bottom: 1px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 14px;">
                        <div><b>De:</b> prevencao@seguroscloudio.com.br</div>
                        <div><b>Para:</b> {notif_selecionada.segurado_email}</div>
                        <div><b>Assunto:</b> {notif_selecionada.titulo}</div>
                    </div>
                    <div style="white-space: pre-line; font-size: 0.95rem; color: #334155; line-height: 1.5;">
                        {notif_selecionada.mensagem_texto}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("Execute primeiro um cenário de risco na aba **'⚡ Demonstração do Pipeline'** para visualizar os canais aqui.")

# ==============================================================================
# ABA 3: BASE DE SEGURADOS & APÓLICES
# ==============================================================================
with tab3:
    st.subheader("👥 Base de Clientes Segurados e Carteira de Apólices")
    st.markdown("Consulte a base cadastral de segurados distribuída por cidades brasileiras e ramos de seguro.")

    dados_tabela = []
    for s in segurados:
        for a in s.apolices:
            dados_tabela.append({
                "ID Cliente": s.id,
                "Nome do Segurado": s.nome,
                "Cidade/UF": f"{s.cidade} - {s.estado}",
                "Bairro": s.bairro,
                "Canal Preferencial": s.canal_preferencial.value,
                "ID Apólice": a.id,
                "Ramo": a.tipo_ramo.value,
                "Bem Assegurado": a.descricao_bem,
                "Valor Segurado (R$)": a.valor_assegurado_reais,
                "Franquia (R$)": a.franquia_reais,
                "Coberturas": ", ".join(a.coberturas)
            })

    df_segurados = pd.DataFrame(dados_tabela)

    # Filtros
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filtro_ramo = st.multiselect("Filtrar por Ramo:", df_segurados["Ramo"].unique())
    with f_col2:
        filtro_cidade = st.multiselect("Filtrar por Cidade:", df_segurados["Cidade/UF"].unique())
    with f_col3:
        filtro_canal = st.multiselect("Filtrar por Canal:", df_segurados["Canal Preferencial"].unique())

    df_filtrado = df_segurados.copy()
    if filtro_ramo:
        df_filtrado = df_filtrado[df_filtrado["Ramo"].isin(filtro_ramo)]
    if filtro_cidade:
        df_filtrado = df_filtrado[df_filtrado["Cidade/UF"].isin(filtro_cidade)]
    if filtro_canal:
        df_filtrado = df_filtrado[df_filtrado["Canal Preferencial"].isin(filtro_canal)]

    st.dataframe(
        df_filtrado.style.format({
            "Valor Segurado (R$)": "R$ {:,.2f}",
            "Franquia (R$)": "R$ {:,.2f}"
        }),
        use_container_width=True,
        height=380
    )

# ==============================================================================
# ABA 4: PAINEL EXECUTIVO & MÉTRICAS
# ==============================================================================
with tab4:
    st.subheader("📊 Painel Executivo de Eficiência e Prevenção de Sinistros")
    st.markdown("Métricas consolidadas de ROI da prevenção proativa de sinistros via Inteligência Artificial.")

    if "ultimo_resultado" in st.session_state:
        res = st.session_state["ultimo_resultado"]
        met = res.metricas

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-box">
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">Economia em Sinistros Prevenidos</div>
                <div style="color: #059669; font-size: 1.8rem; font-weight: 700; margin-top: 6px;">R$ {met.economia_sinistros_estimada_reais:,.2f}</div>
                <div style="color: #10b981; font-size: 0.8rem; margin-top: 4px;">📈 Estimativa de perdas evitadas</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-box">
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">Notificações Disparadas</div>
                <div style="color: #0284c7; font-size: 1.8rem; font-weight: 700; margin-top: 6px;">{met.total_notificacoes_geradas}</div>
                <div style="color: #38bdf8; font-size: 0.8rem; margin-top: 4px;">🎯 100% no canal preferencial</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-box">
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">Clientes Protegidos</div>
                <div style="color: #7c3aed; font-size: 1.8rem; font-weight: 700; margin-top: 6px;">{met.total_segurados_em_risco}</div>
                <div style="color: #a78bfa; font-size: 0.8rem; margin-top: 4px;">👥 De {met.total_segurados_avaliados} avaliados</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-box">
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">Tempo de Resposta do Pipeline</div>
                <div style="color: #d97706; font-size: 1.8rem; font-weight: 700; margin-top: 6px;">{met.tempo_execucao_segundos:.2f}s</div>
                <div style="color: #fbbf24; font-size: 0.8rem; margin-top: 4px;">⚡ 5 agentes orquestrados</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("#### 📱 Distribuição das Notificações por Canal")
            if met.distribuicao_canais:
                df_c = pd.DataFrame(list(met.distribuicao_canais.items()), columns=["Canal", "Quantidade"])
                st.bar_chart(df_c.set_index("Canal"))
            else:
                st.info("Nenhuma notificação no último ciclo.")

        with g2:
            st.markdown("#### 🛡️ Distribuição por Ramo de Seguro")
            if met.distribuicao_ramos:
                df_r = pd.DataFrame(list(met.distribuicao_ramos.items()), columns=["Ramo", "Quantidade"])
                st.bar_chart(df_r.set_index("Ramo"))
            else:
                st.info("Nenhuma notificação no último ciclo.")
    else:
        st.info("Execute uma simulação na aba **'⚡ Demonstração do Pipeline'** para visualizar as métricas executivas.")

# ==============================================================================
# ABA 5: GUIA DIDÁTICO & ARQUITETURA
# ==============================================================================
with tab5:
    st.subheader("📚 Guia Didático para Iniciantes: Como Funciona a Solução?")
    st.markdown("""
    ### 🎯 O Desafio
    Tradicionalmente, a relação entre seguradora e segurado é **reativa**: o cliente só entra em contato após a ocorrência de um sinistro (carro danificado por granizo, casa alagada por enchente, lavoura destruída por geada).
    
    A nossa solução implementa uma **abordagem preventiva e proativa**, antecipando ameaças climáticas e enviando orientações práticas e personalizadas para que o segurado proteja seus bens **antes** do dano acontecer.

    ---

    ### 🏗️ Arquitetura Multiagente Especializada
    
    A solução é dividida em **5 agentes inteligentes**, cada um com uma responsabilidade clara:
    
    1. **Agente Coletor Meteorológico**: Conecta-se à API pública global **Open-Meteo** (sem necessidade de chaves de API) e monitora variáveis como precipitação, vento, granizo e temperatura.
    2. **Agente Analisador de Risco Climático**: Avalia as leituras com base em limiares técnicos da **Defesa Civil / INMET** e classifica o risco em *Baixo, Médio, Alto ou Crítico*.
    3. **Agente de Regras de Negócio**: Cruza a localização do alerta com a base de segurados, avaliando o ramo do seguro (Auto, Residencial, Agro, Empresarial) e as coberturas contratuais.
    4. **Agente de Comunicação Proativa com IA**: Redige mensagens humanizadas, empáticas e acionáveis utilizando Modelos de Linguagem Generativa (**Google Gemini / OpenAI / Motor Didático**).
    5. **Agente Simulador de Envio e Auditoria**: Simula a entrega multicanal (**WhatsApp, SMS, Push, E-mail**), registra logs de auditoria e calcula métricas de sinistros evitados.

    ---

    ### 💻 Tecnologias Utilizadas
    - **Linguagem:** Python 3.11+
    - **Framework Web:** Streamlit
    - **IA Generativa:** Google Gemini API / OpenAI API / Motor Didático Resiliente
    - **Dados Meteorológicos:** Open-Meteo Public API
    - **Validação de Dados:** Pydantic
    - **Visualização & CLI:** Rich
    - **Geração de Relatórios:** FPDF2 / PyMuPDF
    - **Testes Automatizados:** Pytest
    """)

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 10px;'>"
    "Seguros CloudIO • Desafio 5 - Instituto de Inteligência Artificial Aplicada (I2A2) • Licença MIT"
    "</div>",
    unsafe_allow_html=True
)
