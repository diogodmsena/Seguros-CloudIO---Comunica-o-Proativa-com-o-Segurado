# 📖 Guia de Operação da Interface Web - Seguros CloudIO

> **Desafio 5 - Instituto de Inteligência Artificial Aplicada (I2A2)**  
> *Ferramenta Inteligente para Comunicação Proativa com o Segurado utilizando Arquitetura Multiagente e IA Generativa.*

---

## 🎯 1. Visão Geral da Interface

A interface web do **Seguros CloudIO** foi desenvolvida em **Streamlit**, oferecendo uma experiência moderna, interativa e altamente didática. O sistema permite simular em tempo real todo o ciclo de vida da prevenção securitária: desde a captura de eventos meteorológicos até o envio de orientações práticas no smartphone do cliente.

A aplicação está organizada em **5 abas navegáveis**:
1. **⚡ Demonstração do Pipeline Multiagente:** Painel de controle para disparar simulações ou consultas em tempo real e acompanhar o raciocínio de cada agente.
2. **📱 Simulador de Notificações nos Canais:** Visualizador imersivo em formato de smartphone (WhatsApp, SMS, Push e E-mail).
3. **👥 Base de Segurados & Apólices:** Tabela exploratória com filtros por ramo de seguro, cidade e canal de comunicação.
4. **📊 Painel Executivo & Métricas:** Dashboard executivo com cálculo do ROI da prevenção, sinistros evitados e gráficos analíticos.
5. **📚 Guia Didático & Arquitetura:** Documentação embutida sobre os agentes e o edital do Desafio 5 (I2A2).

---

## 🚀 2. Como Iniciar a Aplicação Web

### Passo 1: Abrir o Terminal na Pasta do Projeto
Abra o PowerShell ou Prompt de Comando no diretório raiz do projeto:
```bash
cd "d:\projects\Insur Minds\Desafio 5"
```

### Passo 2: Ativar o Ambiente Virtual
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### Passo 3: Executar o Streamlit
Inicie o servidor local com o comando:
```bash
streamlit run app.py
```

### Passo 4: Acessar no Navegador
A aplicação abrirá automaticamente no seu navegador padrão. Caso não abra, acesse a URL:
👉 **`http://localhost:8501`**

> [!NOTE]
> O sistema funciona **100% offline** graças ao **Motor Generativo Didático Local**. Caso deseje utilizar modelos em nuvem como Google Gemini ou OpenAI, basta configurar as chaves no arquivo `.env`.

---

## 🖥️ 3. Guia Operacional Passo a Passo por Aba

---

### Aba 1: ⚡ Demonstração do Pipeline Multiagente

Esta é a tela principal de operação, onde você configura as condições de entrada e aciona os agentes inteligentes.

```
┌───────────────────────────────┐  ┌─────────────────────────────────────────────────────┐
│ ⚙️ Configuração da Demonstração│  │ 📍 Condições Meteorológicas & Rastros dos Agentes   │
│                               │  │                                                     │
│ (o) Cenários Simulados        │  │ [🌧️ Precipitação] [💨 Vento] [🧊 Granizo] [🌡️ Temp] │
│ ( ) API Open-Meteo            │  │                                                     │
│                               │  │ 🤖 Passo 1: Coletor Meteorológico (OK)              │
│ [ Selecionar Cenário...     ] │  │ 🤖 Passo 2: Análise de Risco (OK)                   │
│                               │  │ 🤖 Passo 3: Regras de Negócio (OK)                  │
│ [ 🚀 Executar Pipeline ]      │  │ 🤖 Passo 4: Redação Proativa com IA (OK)            │
│                               │  │ 🤖 Passo 5: Simulador de Despacho (OK)              │
└───────────────────────────────┘  └─────────────────────────────────────────────────────┘
```

#### Passo a Passo para Operar:
1. **Escolha a Fonte de Dados na coluna esquerda:**
   - **🌦️ Cenários Simulados Didáticos (Recomendado):** Permite reproduzir condições extremas com impacto garantido em apólices da base:
     - `CENARIO-01`: Chuva Torrencial em São Paulo / SP (Risco Crítico de Alagamento - Ramo Residencial e Auto).
     - `CENARIO-02`: Tempestade de Granizo em Caxias do Sul / RS (Risco Alto de Granizo - Ramo Auto).
     - `CENARIO-03`: Geada Severa em Porto Alegre / RS (Risco Alto de Geada - Ramo Agro).
     - `CENARIO-04`: Vendaval Severo em Curitiba / PR (Risco Médio de Vendaval - Ramo Residencial e Empresarial).
     - `CENARIO-05`: Dia Ensolarado / Estável em Belo Horizonte / MG (Condição Segura - Sem disparo de alertas).
   - **📡 API Open-Meteo em Tempo Real:** Consulta a previsão climática atualizada via internet para qualquer uma das capitais brasileiras cadastradas.
2. **Clique no botão:**  
   👉 **`🚀 Executar Pipeline Multiagente`**
3. **Analise os Resultados na coluna direita:**
   - **Métricas Meteorológicas:** Veja precipitação acumulada, velocidade das rajadas de vento, risco percentual de granizo e temperatura.
   - **Rastreamento do Raciocínio dos Agentes:** Expanda cada passo para verificar quanto tempo (em milissegundos) o agente levou e quais regras foram ativadas.
   - **Cards de Notificação Gerada:** Veja os segurados impactados, a severidade do risco, a apólice cruzada e uma prévia da mensagem com o feedback simulado do cliente.

---

### Aba 2: 📱 Simulador de Notificações nos Canais (Smartphone View)

Esta aba permite auditar a experiência final do segurado, renderizando um dispositivo móvel interativo com o formato exato de cada meio de comunicação.

#### Passo a Passo para Operar:
1. Certifique-se de já ter executado uma simulação na **Aba 1**.
2. Na coluna esquerda, use o campo **"Selecione o Segurado para Visualização"** para alternar entre os segurados que receberam notificações.
3. Observe os dados cadastrais do cliente selecionado:
   - Contatos (telefone e e-mail).
   - Bem segurado e apólice vinculada.
   - **Economia Estimada em Sinistro:** O valor financeiro preservado pela ação preventiva.
   - **Checklist de Ações Preventivas:** A lista didática de 3 a 5 passos recomendados ao segurado.
4. Na coluna direita, veja a tela do smartphone renderizada de acordo com o canal preferencial do segurado:
   - 🟢 **WhatsApp:** Exibe a mensagem formatada com emojis, negrito, horário de entrega, selo de verificação da seguradora e botões de suporte 24h.
   - 🔵 **SMS:** Formato conciso e direto, ideal para situações onde a conexão de dados móveis pode estar instável.
   - 🟣 **Push Notification:** Visual escuro típico das notificações da tela de bloqueio do smartphone.
   - ✉️ **E-mail:** Layout formal e acolhedor, contendo cabeçalho institucional completo e orientações detalhadas.

---

### Aba 3: 👥 Base de Segurados & Apólices

Permite consultar e explorar a carteira de segurados que abastece o Agente de Regras de Negócio.

#### Passo a Passo para Operar:
1. Utilize os filtros interativos no topo da página:
   - **Filtrar por Ramo:** Selecione `Automóvel`, `Residencial`, `Agropecuário` ou `Empresarial`.
   - **Filtrar por Cidade:** Filtre por municípios específicos (ex: São Paulo, Caxias do Sul, Porto Alegre).
   - **Filtrar por Canal Preferencial:** Selecione `WhatsApp`, `SMS`, `Push` ou `E-mail`.
2. Observe na tabela os valores assegurados, franquias contratuais e coberturas ativas para cada cliente.

---

### Aba 4: 📊 Painel Executivo & Métricas (ROI da Prevenção)

Apresenta indicadores de desempenho (KPIs) voltados à diretoria executiva e gestão de sinistralidade.

#### Principais Indicadores Exibidos:
- 💰 **Economia em Sinistros Prevenidos:** Soma estimada do prejuízo evitado pelas ações preventivas adotadas pelos clientes antes da tempestade.
- 📬 **Notificações Disparadas:** Total de mensagens despachadas aos segurados sob ameaça climática iminente.
- 👥 **Clientes Protegidos:** Quantidade de pessoas salvas de prejuízos materiais e transtornos.
- ⚡ **Tempo de Resposta do Pipeline:** Duração total da esteira multiagente (geralmente inferior a 1 segundo).
- 📈 **Gráficos Dinâmicos:**
  - *Distribuição por Canal de Envio:* Volume de notificações entre WhatsApp, SMS, Push e E-mail.
  - *Distribuição por Ramo de Seguro:* Segmentação dos riscos prevenidos por tipo de patrimônio.

---

### Aba 5: 📚 Guia Didático & Arquitetura

Serve como material de apoio para apresentações, bancas avaliadoras e novos usuários:
- Explica o problema de negócio (modelo reativo vs. preventivo).
- Detalha a função e responsabilidade de cada um dos 5 agentes da esteira.
- Apresenta o diagrama funcional da esteira e a lista de bibliotecas do ecossistema.

---

## 💡 4. Roteiro Recomendado para Apresentações / Demonstrações

Para demonstrar a solução de forma impactante em **3 minutos**, siga esta sequência:

1. **Passo 1 (Cenário de Granizo):**
   - Acesse a **Aba 1**.
   - Escolha o cenário `CENARIO-02 - Tempestade Severa de Granizo (Caxias do Sul - RS)`.
   - Clique em **"Executar Pipeline Multiagente"**.
   - Mostre os 5 agentes executando em sequência e o Agente de Regras cruzando a ameaça de granizo com as apólices do ramo **Automóvel**.
2. **Passo 2 (Experiência no Smartphone):**
   - Vá para a **Aba 2**.
   - Selecione a segurada **Camila Rocha**.
   - Mostre como o alerta do WhatsApp orienta a guardar o carro em garagem coberta ou usar capas acolchoadas.
3. **Passo 3 (Cenário Seguro / Descarte):**
   - Volte para a **Aba 1**.
   - Selecione `CENARIO-05 - Dia Ensolarado e Estável (Belo Horizonte - MG)`.
   - Execute o pipeline e mostre que o sistema é inteligente para **não disparar mensagens desnecessárias**, evitando fadiga de notificações.
4. **Passo 4 (Impacto Financeiro):**
   - Acesse a **Aba 4**.
   - Mostre as métricas de sinistros evitados e o tempo de execução em milissegundos.

---

## ❓ 5. Resolução de Dúvidas Comuns (FAQ)

### Como testar com a previsão do tempo real da minha cidade?
Na **Aba 1**, mude a opção de rádio para **"📡 API Open-Meteo em Tempo Real"** e escolha uma das capitais disponíveis. O sistema fará a requisição HTTP imediata aos servidores meteorológicos globais.

### É obrigatório ter chave da OpenAI ou do Google Gemini?
**Não.** O projeto vem equipado com um motor generativo local inteligente e determinístico, desenvolvido para permitir que qualquer pessoa teste a solução imediatamente sem custos ou configurações extras.

### Como reiniciar ou limpar o cache do Streamlit?
- Pressione a tecla **`R`** no navegador para recarregar a interface.
- Pressione a tecla **`C`** para limpar o cache da aplicação caso modifique algum arquivo JSON.

---

*Seguros CloudIO — Inovação, Cuidado e Inteligência Artificial a favor do segurado.*
