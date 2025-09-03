# Clima.AI

## 🌤️ Sistema de Agentes Inteligentes para Dados Climáticos

Um sistema profissional de chatbot com LLM que responde com base nos dados climáticos da iCrop, utilizando uma arquitetura de agentes especializados e bem organizados.

### 🏗️ Arquitetura do Sistema

O sistema é composto por **4 agentes especializados** coordenados por um **orquestrador principal**:

#### 🤖 **Agentes Especializados:**

1. **🔍 Question Classifier Agent**
   - Classifica o tipo de pergunta do usuário
   - Identifica se precisa de estação específica
   - Tipos: Listar estações, Clima atual, Previsão, Dados por hora, Análise geral

2. **📡 Station Identifier Agent**
   - Identifica estações por nome ou ID
   - Busca todas as estações disponíveis
   - Valida existência da estação

3. **📊 Climate Data Agent**
   - Busca dados climáticos da API iCrop
   - Formata dados para exibição
   - Trata erros de conexão

4. **🧠 LLM Analysis Agent**
   - Análise inteligente com OpenRouter
   - Interpretação de dados climáticos
   - Respostas contextuais

#### 🎯 **Orquestrador Principal:**
- **ClimateChatOrchestrator**: Coordena todos os agentes em sequência
- Gerencia o fluxo de processamento
- Fornece status do sistema

### 📁 Estrutura do Projeto

```
Clima.AI/
├── app.py                    # Aplicativo Streamlit principal
├── orchestrator.py           # Orquestrador dos agentes
├── config.py                 # Configurações centralizadas
├── config.env                # Variáveis de ambiente
├── requirements.txt          # Dependências
├── README.md                 # Documentação
└── agents/                   # Pacote de agentes
    ├── __init__.py
    ├── question_classifier.py
    ├── station_identifier.py
    ├── climate_data.py
    └── llm_analysis.py
```

### 🚀 Como executar

1. **Instalar dependências:**
```bash
conda install streamlit requests pandas python-dotenv -y
```

2. **Executar o aplicativo:**
```bash
streamlit run app.py
```

3. **Acessar no navegador:**
O aplicativo será aberto automaticamente em `http://localhost:8501`

### 🔧 Configuração

#### **Variáveis de Ambiente (config.env):**
```env
# API iCrop
ICROP_API_KEY=f64ca436be34ea5a7c621facf63733b947260af56d3a3ab85c8ea3278a617225
ICROP_BASE_URL=https://performance.icrop.online/homologacao/rest/v1/data

# API OpenRouter
OPENROUTER_API_KEY=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
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
```

### 🔄 Fluxo de Processamento

1. **Entrada do Usuário** → Pergunta no chat
2. **Question Classifier** → Identifica tipo de pergunta
3. **Station Identifier** → Identifica estação (se necessário)
4. **Climate Data** → Busca dados da API iCrop
5. **LLM Analysis** → Análise inteligente (se necessário)
6. **Orquestrador** → Coordena e retorna resposta

### 📋 Funcionalidades

#### **Estações:**
- ✅ Listar todas as estações disponíveis
- ✅ Identificar estação por nome ou ID
- ✅ Validação de existência

#### **Dados Climáticos:**
- ✅ Dados atuais (temperatura, umidade, chuva, vento, radiação)
- ✅ Previsões do tempo
- ✅ Dados por hora
- ✅ Formatação profissional

#### **Análise Inteligente:**
- ✅ Interpretação de dados climáticos
- ✅ Respostas contextuais
- ✅ Análise de tendências

### 🎯 Exemplos de Uso

#### **Estações:**
- "Quais estações estão disponíveis?"
- "Liste todas as estações"

#### **Dados Climáticos:**
- "Quero saber o clima da estação Bradesco"
- "Temperatura da estação ID: 2297"
- "Como está o clima agora na estação Estrela"

#### **Previsões:**
- "Previsão para amanhã da estação Bradesco"
- "Como estará o tempo na estação ID: 2296"

#### **Análises:**
- "Analise os dados climáticos"
- "Qual a tendência da temperatura?"

### 🌟 Vantagens da Arquitetura

- **Modularidade:** Cada agente tem responsabilidade específica
- **Escalabilidade:** Fácil adicionar novos agentes
- **Manutenibilidade:** Código organizado e bem documentado
- **Confiabilidade:** Tratamento de erros em cada camada
- **Flexibilidade:** Agentes podem ser reutilizados

### 🔍 Monitoramento

O sistema inclui:
- ✅ Status em tempo real dos agentes
- ✅ Contagem de estações disponíveis
- ✅ Indicadores de saúde do sistema
- ✅ Tratamento de erros centralizado

### 🛠️ Desenvolvimento

#### **Adicionar Novo Agente:**
1. Criar arquivo em `agents/`
2. Implementar interface padrão
3. Registrar no `__init__.py`
4. Integrar no orquestrador

#### **Modificar Configurações:**
- Editar `config.py` para novas variáveis
- Atualizar `config.env` para valores
- Validar com `Config.validate()`

---

*Sistema profissional de agentes inteligentes para dados climáticos em tempo real*