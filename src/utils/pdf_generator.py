"""
Gerador de Relatório Técnico em PDF para o Desafio 5 (I2A2).
Gera um documento técnico formatado e profissional compatível com todos os ambientes.
"""

import os
import re
from pathlib import Path
from fpdf import FPDF
from src.config import RELATORIO_PDF, RELATORIO_MD


def obter_integrantes(caminho_md: Path = RELATORIO_MD) -> list[tuple[str, str, str]]:
    """Extrai a lista de integrantes a partir de relatorio_tecnico.md ou retorna os dados padrão."""
    integrantes_padrao = [
        ("Isabel de Castro Beneyto", "(85) 98630-5456", "castrobeneyto@gmail.com"),
        ("Adolfo Emmanuel Correa López", "(21) 97240-9801", "adolfo.correa.lopez@gmail.com"),
        ("Jessica Mayumi Odo Bastos", "(11) 95216-6175", "jessica.odo03@gmail.com"),
        ("Diogo David Macêdo Sena", "(84) 99982-4141", "diogodmsena@gmail.com"),
    ]
    if not caminho_md.exists():
        return integrantes_padrao

    try:
        conteudo = caminho_md.read_text(encoding="utf-8")
        match = re.search(r"\*\*Integrantes:\*\*(.*?)(?:---|\n##|\Z)", conteudo, re.DOTALL)
        if not match:
            return integrantes_padrao

        linhas = [l.strip() for l in match.group(1).strip().splitlines() if l.strip()]
        resultado = []
        for linha in linhas:
            linha_limpa = linha.lstrip("-*• ").strip()
            partes = [p.strip() for p in linha_limpa.split(" - ")]
            if len(partes) >= 3:
                resultado.append((partes[0], partes[1], partes[2]))

        return resultado if resultado else integrantes_padrao
    except Exception:
        return integrantes_padrao


def sanitizar_texto_latin1(texto: str) -> str:
    """Substitui caracteres especiais e emojis por representações equivalentes compatíveis com Latin-1."""
    substituicoes = {
        "•": "-",
        "✓": "[OK]",
        "⚠️": "[ALERTA]",
        "👋": "",
        "🛡️": "",
        "📋": "",
        "⛈️": "",
        "💡": "",
        "1️⃣": "1)",
        "2️⃣": "2)",
        "3️⃣": "3)",
        "4️⃣": "4)",
        "5️⃣": "5)",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "→": "->",
        "➔": "->",
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    
    # Remove qualquer caractere fora do alcance Latin-1 para evitar exceções
    return texto.encode("latin-1", "replace").decode("latin-1")


class RelatorioTecnicoPDF(FPDF):
    """Classe personalizada para o Relatório Técnico com cabeçalho e rodapé estilizados."""

    def header(self):
        # Barra superior azul
        self.set_fill_color(3, 105, 161)  # Azul escuro
        self.rect(0, 0, 210, 15, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        self.set_xy(10, 3)
        self.cell(0, 10, sanitizar_texto_latin1("Instituto de Inteligência Artificial Aplicada - I2A2 | Desafio 5"), 0, 0, 'L')
        self.cell(0, 10, "Seguros CloudIO", 0, 1, 'R')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}} - Relatorio Tecnico Desafio 5", 0, 0, 'C')

    def chapter_title(self, num, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.set_fill_color(241, 245, 249)
        self.cell(0, 8, sanitizar_texto_latin1(f"{num}. {title}"), 0, 1, 'L', fill=True)
        self.ln(2)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(2, 132, 199)
        self.cell(0, 6, sanitizar_texto_latin1(title), 0, 1, 'L')
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5, sanitizar_texto_latin1(text))
        self.ln(2)

    def code_box(self, text):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(248, 250, 252)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 4.5, sanitizar_texto_latin1(text), border=1, fill=True)
        self.ln(2)


def gerar_pdf_relatorio(caminho_saida: Path = RELATORIO_PDF) -> Path:
    """Gera o arquivo PDF do relatório técnico oficial do projeto."""
    pdf = RelatorioTecnicoPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=18)

    # Título Principal
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 9, sanitizar_texto_latin1("Relatório Técnico da Solução"), 0, 1, 'C')
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(3, 105, 161)
    pdf.cell(0, 5, sanitizar_texto_latin1("Ferramenta Inteligente para Comunicação Proativa com o Segurado"), 0, 1, 'C')
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4.5, sanitizar_texto_latin1("Desafio 5 - Instituto de Inteligência Artificial Aplicada (I2A2) | Projeto: Seguros CloudIO"), 0, 1, 'C')
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.cell(0, 4.5, sanitizar_texto_latin1("Data: Setembro / 2026 | Licença: MIT"), 0, 1, 'C')
    pdf.ln(3)

    # Bloco dos Integrantes (referência: relatorio_tecnico.md)
    integrantes = obter_integrantes()
    x_box = 10
    y_box = pdf.get_y()
    w_box = 190
    h_box = 8 + (len(integrantes) * 5)

    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(x_box, y_box, w_box, h_box, 'DF')

    pdf.set_xy(x_box + 4, y_box + 2.5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 4.5, sanitizar_texto_latin1("Integrantes:"), 0, 1, 'L')

    for nome, tel, email in integrantes:
        pdf.set_x(x_box + 6)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(3.5, 4.5, chr(149), 0, 0, 'L')
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(pdf.get_string_width(sanitizar_texto_latin1(nome)) + 1, 4.5, sanitizar_texto_latin1(nome), 0, 0, 'L')
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(71, 85, 105)
        sep_tel = f" - {tel} - "
        pdf.cell(pdf.get_string_width(sep_tel) + 1, 4.5, sep_tel, 0, 0, 'L')
        pdf.set_text_color(2, 132, 199)
        pdf.cell(pdf.get_string_width(email) + 1, 4.5, email, 0, 1, 'L', link=f"mailto:{email}")

    pdf.set_y(y_box + h_box + 4)

    # 1. Objetivo e Visão Geral
    pdf.chapter_title(1, "Objetivo e Visão Geral da Solução")
    pdf.body_text(
        "Grande parte das interações entre seguradoras e clientes acontece tradicionalmente apenas após a ocorrência de um sinistro (modelo reativo). "
        "Este projeto implementa uma solução baseada em Inteligência Artificial e Arquitetura Multiagente que transforma esse paradigma em uma "
        "abordagem preventiva e consultiva. O sistema monitora variáveis meteorológicas em tempo real através de APIs públicas, "
        "identifica eventos de risco iminentes (chuvas torrenciais, granizo, vendavais e geadas), cruza os dados com a carteira de segurados e apólices, "
        "e gera comunicações altamente personalizadas e empáticas com orientações práticas para a proteção patrimonial antes que o sinistro ocorra."
    )

    # 2. Arquitetura da Solução
    pdf.chapter_title(2, "Arquitetura da Solução Multiagente")
    pdf.body_text(
        "A solução adota uma Arquitetura Multiagente Especializada e modular, onde cada agente possui papéis e responsabilidades bem definidos:"
    )
    pdf.code_box(
        "+-------------------------------------------------------------------------+\n"
        "|                 ESTEIRA DE ORQUESTRACAO MULTIAGENTE                     |\n"
        "+-------------------------------------------------------------------------+\n"
        " [Fonte: Open-Meteo API / Cenarios] ---> 1. Agente Coletor Meteorologico\n"
        "                                                    |\n"
        "                                         2. Agente de Analise de Risco\n"
        "                                                    |\n"
        "                                         3. Agente de Regras de Negocio\n"
        "                                                    |\n"
        "                                         4. Agente Comunicador IA (LLM)\n"
        "                                                    |\n"
        "                                         5. Agente Simulador de Despacho\n"
        "                                                    |\n"
        "                                         [Dashboard Web / Smartphone UI]\n"
        "+-------------------------------------------------------------------------+"
    )

    # 3. Descrição Detalhada dos Agentes
    pdf.chapter_title(3, "Descrição dos Agentes Especializados")
    
    pdf.sub_title("3.1 Agente Coletor Meteorológico (Weather Collector Agent)")
    pdf.body_text(
        "- Responsabilidade: Realizar consultas à API pública global Open-Meteo ou carregar cenários simulados pré-configurados.\n"
        "- Entradas: Coordenadas geográficas (latitude/longitude) ou nome da cidade.\n"
        "- Saídas: Objeto estruturado EventoClimatico contendo precipitação (mm/h), rajadas de vento (km/h), probabilidade de granizo (%), temperatura e descrição da condição."
    )

    pdf.sub_title("3.2 Agente de Análise de Riscos Climáticos (Climate Risk Analyzer Agent)")
    pdf.body_text(
        "- Responsabilidade: Analisar leituras climáticas contra matrizes e limiares técnicos da Defesa Civil e INMET.\n"
        "- Lógica de Classificação: Avalia risco de Chuva Intensa (>=15mm), Vento Forte (>=45km/h), Granizo (probabilidade >=20%) e Geada (<=8°C), classificando em Baixo, Médio, Alto ou Crítico.\n"
        "- Saídas: Lista de objetos AlertaRisco com diagnósticos e justificativas técnicas."
    )

    pdf.sub_title("3.3 Agente Especialista em Regras de Negócio (Insurance Business Rules Agent)")
    pdf.body_text(
        "- Responsabilidade: Filtrar a base de clientes segurados expostos ao evento climático por geolocalização e ramo de atuação (Auto, Residencial, Agro, Empresarial).\n"
        "- Matriz de Decisão: Valida se a apólice possui relevância para o tipo de perigo (ex: Seguro Auto para risco de granizo; Seguro Residencial para alagamento).\n"
        "- Saídas: Conjunto de tuplas (Segurado, Apólice, Alerta, Canal) aprovadas para envio preventivo."
    )

    pdf.sub_title("3.4 Agente de Comunicação Proativa com IA (Generative Copywriter Agent)")
    pdf.body_text(
        "- Responsabilidade: Utilizar Modelos de Linguagem Generativa (Google Gemini API, OpenAI ou Motor Didático Local) para redigir a mensagem.\n"
        "- Diretrizes de Redação: Tom empático, acolhedor e ágil; inclusão do nome do segurado, identificação do bem assegurado e fornecimento de checklist prático com 3 a 5 ações de segurança imediatas."
    )

    pdf.sub_title("3.5 Agente Simulador de Envio e Auditoria (Notification Dispatch Agent)")
    pdf.body_text(
        "- Responsabilidade: Simular o roteamento e entrega nos canais (WhatsApp, SMS, Push Notification, E-mail), capturar feedbacks simulados e computar indicadores econômicos (economia estimada em sinistros evitados e tempo de resposta)."
    )

    # 4. Tecnologias Utilizadas
    pdf.chapter_title(4, "Tecnologias e Bibliotecas Utilizadas")
    pdf.body_text(
        "- Python 3.11+: Linguagem base para desenvolvimento backend e agentes.\n"
        "- Streamlit: Interface visual web interativa com simulador de celular e painel executivo.\n"
        "- Pydantic: Validação de dados, tipagem estática e serialização de modelos.\n"
        "- Open-Meteo API: Fonte pública global de previsão do tempo em tempo real (zero chaves necessárias).\n"
        "- Google GenAI / OpenAI SDKs: Integração com LLMs generativos de ponta com fallback local.\n"
        "- Rich: Formatação rica de terminal CLI com árvores de decisão e tabelas coloridas.\n"
        "- FPDF2 / PyMuPDF: Geração e manipulação automatizada de relatórios em PDF.\n"
        "- Pytest: Suíte de testes automatizados para garantia de qualidade do software."
    )

    # 5. Exemplos de Mensagens Geradas
    pdf.chapter_title(5, "Exemplos de Comunicações Preventivas Geradas")

    pdf.sub_title("Cenário A: Queda Severa de Granizo em Curitiba (Ramo Auto - WhatsApp)")
    pdf.code_box(
        "Olá, Mariana! \n"
        "Nossa central de inteligência climática identificou um alerta de Queda de Granizo com severidade CRÍTICO para a sua região em Curitiba.\n"
        "Patrimônio Protegido: Jeep Compass Longitude 2024 (Apólice APO-1003)\n"
        "Recomendações preventivas imediatas:\n"
        "1) Estacione o seu Jeep Compass em garagem coberta ou estacionamento subterrâneo nas próximas horas.\n"
        "2) Evite estacionar sob árvores com galhos secos ou postes de fiação exposta.\n"
        "3) Se surpreendido na via, reduza a velocidade e procure abrigo sob postos de combustível com segurança.\n"
        "Sua apólice conta com cobertura completa para granizo e vidros. Central 24h: 0800-700-SAFE."
    )

    pdf.sub_title("Cenário B: Chuva Torrencial e Alagamento em São Paulo (Ramo Residencial - WhatsApp)")
    pdf.code_box(
        "Olá, Carlos! \n"
        "Nossa central identificou alerta de Chuva Intensa / Alagamento (CRÍTICO) para a Vila Madalena em São Paulo (65 mm/h).\n"
        "Patrimônio Protegido: Casa Térrea com Jardim (Apólice APO-1002)\n"
        "Recomendações preventivas imediatas:\n"
        "1) Verifique e desobstrua calhas, ralos e grelhas de escoamento do imóvel.\n"
        "2) Desconecte aparelhos eletrônicos sensíveis da tomada para evitar danos elétricos.\n"
        "3) Coloque móveis e documentos importantes em locais elevados caso more em área rebaixada.\n"
        "4) Feche bem janelas, portas e claraboias antes do início da tempestade."
    )

    if pdf.get_y() > 230:
        pdf.add_page()

    pdf.sub_title("Cenário C: Geada Severa no Sul (Ramo Agro - SMS / E-mail)")
    pdf.code_box(
        "Seguros CloudIO Alerta Agro: Risco de Geada Severa (0.5 C) em Porto Alegre / Zona Sul.\n"
        "Proteja sua Lavoura de Trigo e Pomar de Maçãs (Apólice APO-1004).\n"
        "Ações: Acione aspersão preventiva e cubra mudas sensíveis com palha/lona. Abrigue maquinários. Assistência: 0800-700-7233."
    )

    # 6. Conclusão e Critérios Atendidos
    pdf.chapter_title(6, "Conclusão e Atendimento aos Requisitos")
    pdf.body_text(
        "A solução desenvolvida atende integralmente a todos os critérios e entregáveis propostos no Desafio 5 do I2A2:\n"
        "[OK] Integração funcional com fonte externa meteorológica pública (Open-Meteo);\n"
        "[OK] Identificação automática de eventos climáticos de risco com base em limiares técnicos;\n"
        "[OK] Aplicação clara e documentada de regras de negócio securitárias;\n"
        "[OK] Geração de mensagens personalizadas com Inteligência Artificial Generativa;\n"
        "[OK] Simulação do envio de notificações em múltiplos canais (WhatsApp, SMS, Push, E-mail);\n"
        "[OK] Demonstração interativa do fluxo completo via Web Dashboard (Streamlit) e Terminal CLI (Rich);\n"
        "[OK] Código modular, testado com Pytest e distribuído sob licença MIT pública."
    )

    caminho_saida = Path(caminho_saida)
    pdf.output(str(caminho_saida))
    return caminho_saida
