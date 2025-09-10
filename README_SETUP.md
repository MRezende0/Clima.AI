# 🌤️ Clima.AI - Sistema de Inteligência Artificial para Clima

## 🚀 Inicialização Rápida

### Opção 1: Script Automático (Recomendado)
```bash
# Windows - Duplo clique no arquivo:
start_clima_ai.bat

# Ou execute no PowerShell:
.\Start-ClimaAI.ps1
```

### Opção 2: Manual
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py
```

## 📁 Estrutura do Projeto

```
Clima.AI/
├── app.py                 # Aplicação principal Streamlit
├── orchestrator.py        # Orquestrador dos agentes
├── config.py             # Configurações do sistema
├── requirements.txt      # Dependências Python
├── start_clima_ai.bat    # Script de inicialização (Windows)
├── Start-ClimaAI.ps1     # Script PowerShell avançado
├── start_clima_ai.sh     # Script de inicialização (Linux/Mac)
├── clima_config.env      # Configurações do ambiente
└── agents/               # Agentes especializados
    ├── question_classifier.py
    ├── station_identifier.py
    ├── climate_data.py
    ├── llm_analysis.py
    └── request_collector.py
```

## 🔧 Configuração

### Variáveis de Ambiente
As chaves de API estão configuradas no arquivo `config.py`:
- **iCrop API**: Dados climáticos
- **OpenRouter API**: Análise com IA

### Personalização
Edite o arquivo `clima_config.env` para ajustar:
- Caminho do Python
- Porta da aplicação
- Configurações adicionais

## 🌐 Acesso

Após executar, acesse:
- **URL Local**: http://localhost:8501
- **URL de Rede**: http://[seu-ip]:8501

## 💡 Funcionalidades

- **Chat Interativo**: Perguntas sobre clima
- **Agentes Especializados**: Sistema multi-agente
- **Integração APIs**: iCrop + OpenRouter
- **Interface Amigável**: Dashboard com status

## 🛠️ Solução de Problemas

### Python não encontrado
1. Instale Python 3.8+ do site oficial
2. Marque "Add Python to PATH" durante instalação
3. Ajuste o caminho no script se necessário

### Dependências não instalam
1. Execute: `pip install --upgrade pip`
2. Use: `pip install -r requirements.txt --force-reinstall`
3. Para Windows: Instale Microsoft Visual C++ Build Tools

### Porta ocupada
1. Execute: `.\Start-ClimaAI.ps1 -Port 8502`
2. Ou pare outros serviços na porta 8501

## 📞 Suporte

Desenvolvido por: **Geotecnologia Cocal**
