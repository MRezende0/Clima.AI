"""
Aplicativo principal do Clima.AI
"""
import streamlit as st
from config import Config
from orchestrator import ClimateChatOrchestrator

# Configuração da página
st.set_page_config(
    page_title="Clima.AI",
    page_icon="🌤️",
    layout="wide"
)

# Título da aplicação
st.title("🌤️ Clima.AI")
st.markdown("---")

# Inicialização da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Adicionar mensagem inicial do bot
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Olá! O que deseja saber sobre o clima?"
    })

# Inicializar orquestrador apenas uma vez
if "orchestrator" not in st.session_state:
    try:
        Config.validate()
        st.session_state.orchestrator = ClimateChatOrchestrator()
        st.session_state.system_status = st.session_state.orchestrator.get_system_status()
    except Exception as e:
        st.error(f"❌ Erro na configuração: {str(e)}")
        st.stop()

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações do Sistema")
    
    # Status do sistema
    if st.session_state.system_status['status'] == 'operational':
        st.success("✅ Sistema Operacional")
        st.metric("Estações Disponíveis", st.session_state.system_status['stations_count'])
    else:
        st.error("❌ Sistema com Erro")
        st.error(st.session_state.system_status['error'])
    
    st.markdown("### 🤖 Agentes")
    for agent, status in st.session_state.system_status['agents'].items():
        if status == 'active':
            st.success(f"✅ {agent.replace('_', ' ').title()}")
        else:
            st.error(f"❌ {agent.replace('_', ' ').title()}")
    
    st.markdown("---")
    st.markdown("### 📊 APIs Integradas")
    st.markdown("- 🌤️ **iCrop** (Dados Climáticos)")
    st.markdown("- 🤖 **OpenRouter** (IA)")
    
    # Botão para limpar histórico
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        # Adicionar mensagem inicial do bot novamente
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Olá! O que deseja saber sobre o clima?"
        })
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Desenvolvido por:** Geotecnologia Cocal")

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte sobre estações, clima, previsões..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibir mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Exibir indicador de carregamento
    with st.chat_message("assistant"):
        with st.spinner("🤔 Processando com os agentes..."):
            try:
                # Processar pergunta com o orquestrador
                response = st.session_state.orchestrator.process_question(prompt)
                
                # Adicionar resposta ao histórico
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Exibir resposta
                st.markdown(response)
            except Exception as e:
                error_msg = f"❌ Erro no processamento: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.markdown(error_msg)