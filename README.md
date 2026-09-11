# 🛡️ Seguros CloudIO - Ferramenta Inteligente para Comunicação Proativa com o Segurado

> **Desafio 5 - Instituto de Inteligência Artificial Aplicada (I2A2)**  
> *Transformando o modelo reativo de seguros em uma abordagem preventiva com Inteligência Artificial e Arquitetura Multiagente.*

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-green.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)
![Tests](https://img.shields.io/badge/Tests-Pytest%20Passing-brightgreen.svg)

---

## 🎯 1. Visão Geral e Propósito Didático

Tradicionalmente, a relação entre seguradoras e clientes ocorre quase exclusivamente no momento da dor: **após a ocorrência de um sinistro** (um carro avariado por granizo, uma residência inundada, uma safra perdida por geada).

O projeto **Seguros CloudIO** demonstra de forma prática e didática como o uso de **Agentes Inteligentes** e **IA Generativa** permite antecipar riscos climáticos iminentes, orientando o segurado a tomar medidas protetivas simples e eficazes **antes que o dano aconteça**.

### 🌟 Principais Benefícios da Abordagem Preventiva:
- 🛡️ **Proteção do Segurado:** Previne perdas materiais, transtornos e preserva a segurança física da família.
- 📉 **Redução de Sinistros:** Diminui drasticamente os custos operacionais e indenizações das seguradoras.
- ❤️ **Valor Percebido e Fidelização:** Transforma o seguro em um serviço de consultoria e cuidado contínuo.

---

## 🏗️ 2. Arquitetura Multiagente da Solução

O sistema foi desenhado de forma modular, onde cada agente possui um papel de especialista:

```
                  [ 🌐 API Pública Open-Meteo / Cenários Didáticos ]
                                         │
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │ 1. Agente Coletor Meteorológico (Weather Collector Agent)     │
         │    -> Obtém precipitação, ventos, granizo e temperatura       │
         └───────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │ 2. Agente de Análise de Risco (Climate Risk Analyzer Agent)   │
         │    -> Aplica limiares técnicos da Defesa Civil / INMET        │
         └───────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │ 3. Agente de Regras de Negócio (Insurance Business Rules)     │
         │    -> Cruza ativos, localidade e apólices (Auto, Res, Agro)   │
         └───────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │ 4. Agente Comunicador IA (Generative Copywriter Agent)        │
         │    -> Redige mensagens empáticas e checklists com LLM         │
         └───────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
         ┌───────────────────────────────────────────────────────────────┐
         │ 5. Agente Simulador de Despacho (Notification Dispatch Agent) │
         │    -> Roteia por canal (WhatsApp, SMS, Push, E-mail)          │
         └───────────────────────────────┬───────────────────────────────┘
                                         │
                                         ▼
                 [ 📱 Web Dashboard Interativo & Simulador Mobile ]
```

---

## 🚀 3. Como Instalar e Executar

### 📋 Pré-requisitos
- Ter o **Python 3.10 ou superior** instalado na máquina.
- Git instalado (caso queira clonar o repositório).

### 🛠️ Passo 1: Clonar o Repositório ou Extrair o ZIP
```bash
git clone https://github.com/seu-usuario/seguros-cloudio-desafio5.git
cd "seguros-cloudio-desafio5"
```

### 📦 Passo 2: Criar e Ativar um Ambiente Virtual (Recomendado)
```bash
# No Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# No Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

### 📥 Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

---

## 🖥️ 4. Formas de Execução e Demonstração

### Opção A: 🌐 Interface Web Interativa (Streamlit) — **Recomendado**
Inicie o dashboard gráfico completo com simulador de celular, monitor de radar meteorológico e painel executivo:
```bash
streamlit run app.py
```
*O navegador abrirá automaticamente em `http://localhost:8501`.*

### Opção B: 💻 Demonstração Interativa no Terminal (CLI Didático)
Para visualizar o fluxo com árvores de agentes e tabelas coloridas no console:
```bash
python run_demo.py
```

### Opção C: 🧪 Executar a Suíte de Testes Automatizados
Para verificar a integridade de todos os agentes e regras de negócio:
```bash
pytest -v
```

### Opção D: 📄 Gerar o Relatório Técnico em PDF
Gera o relatório formal `relatorio_tecnico.pdf`:
```bash
python generate_report.py
```

### Opção E: 📦 Gerar Pacote ZIP de Entrega
Empacota automaticamente todo o código-fonte, dados e documentação:
```bash
python package_submission.py
```

---

## ⚙️ 5. Configuração de Modelos de IA (Zero-Configuração Necessária)

O projeto possui **três modos de geração de mensagens**:
1. **Motor Generativo Didático Embutido (Padrão - Zero Setup):** Funciona imediatamente sem exigir chaves de API externas, utilizando templates estruturados inteligentes.
2. **Google Gemini API:** Caso queira usar o modelo Gemini da Google, adicione sua chave gratuita no arquivo `.env`:
   ```env
   GEMINI_API_KEY="sua_chave_gemini_aqui"
   LLM_PROVIDER="gemini"
   ```
3. **OpenAI API:** Caso queira usar GPT-4o-mini:
   ```env
   OPENAI_API_KEY="sua_chave_openai_aqui"
   LLM_PROVIDER="openai"
   ```

---

## 📂 6. Estrutura do Projeto

```
Desafio 5/
├── src/
│   ├── __init__.py
│   ├── config.py                  # Configurações globais e limiares técnicos
│   ├── models.py                  # Modelos de dados Pydantic (Segurado, Apólice, Alerta, etc.)
│   ├── data/
│   │   ├── segurados.json         # Base didática de segurados e apólices
│   │   └── cenarios_climaticos.json # Cenários de teste pré-configurados
│   ├── services/
│   │   ├── weather_service.py     # Integração com API Open-Meteo e Geocoding
│   │   └── llm_service.py         # Integração com Gemini, OpenAI e Motor Local
│   ├── agents/
│   │   ├── base_agent.py          # Infraestrutura comum de rastreamento
│   │   ├── collector_agent.py     # Agente 1: Coletor Meteorológico
│   │   ├── risk_agent.py          # Agente 2: Analisador de Risco Climático
│   │   ├── business_rules_agent.py# Agente 3: Regras de Negócio de Seguros
│   │   ├── communication_agent.py # Agente 4: Comunicador Proativo com IA
│   │   ├── dispatcher_agent.py    # Agente 5: Simulador de Envio Multicanal
│   │   └── orchestrator.py        # Orquestrador do Pipeline Multiagente
│   └── utils/
│       └── pdf_generator.py       # Gerador do Relatório Técnico em PDF
├── tests/
│   ├── test_weather_service.py
│   ├── test_risk_analysis.py
│   ├── test_business_rules.py
│   └── test_pipeline.py
├── app.py                         # Aplicação Web Streamlit (Dashboard + Celular)
├── run_demo.py                    # Script CLI interativo no terminal
├── generate_report.py             # Script de compilação do relatório em PDF
├── package_submission.py          # Script gerador do ZIP de entrega
├── relatorio_tecnico.md           # Relatório técnico completo formatado
├── relatorio_tecnico.pdf          # Relatório técnico compilado
├── GUIA_OPERACAO_WEB.md           # Manual de operação passo a passo da interface web
├── requirements.txt               # Dependências do projeto
├── .env.example                   # Exemplo de variáveis de ambiente
├── LICENSE                        # Licença MIT
└── README.md                      # Esta documentação
```

---

## 📜 7. Licença

Este projeto está licenciado sob os termos da **Licença MIT**. Para maiores detalhes, consulte o arquivo [LICENSE](LICENSE).

---
*Desenvolvido pela equipe **Seguros CloudIO** para o **Desafio 5 do Instituto de Inteligência Artificial Aplicada (I2A2)**.*
