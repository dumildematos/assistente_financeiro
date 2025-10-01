# app.py
import streamlit as st
from config import get_gemini_api_key
from services.olx_service import fetch_olx_data
# MUDANÇA: Importa as duas novas funções
from services.gemini_service import start_chat_session, send_message_rest
from app_ui import display_negocios_sidebar, setup_page

# --- Configuração da Página e Avisos ---
setup_page()

# --- Obter Chaves e Tokens ---
api_key = get_gemini_api_key()
bearer_token = st.sidebar.text_input("Seu Bearer Token do OLX", type="password", help="Obtenha este token nas ferramentas de desenvolvedor do seu navegador (F12).")

if not api_key or not bearer_token:
    st.info("Por favor, insira a sua chave de API Gemini e o seu Bearer Token do OLX para começar.")
    st.stop()

# --- Carregar Dados da API e Mostrar Sidebar ---
dados = fetch_olx_data(bearer_token)
if dados:
    display_negocios_sidebar(dados)
else:
    st.warning("Não foi possível obter os dados do OLX. Verifique o token e tente novamente.")
    st.stop()

# --- Inicialização do Chat ---
# MUDANÇA: Agora guardamos o "history" em vez do objeto "chat"
if "history" not in st.session_state:
    with st.spinner("A inicializar o assistente..."):
        model_name = "gemini-pro-latest"
        chat_history, initial_response = start_chat_session(api_key, model_name, dados)
        st.session_state.history = chat_history
        st.session_state.messages = [{"role": "assistant", "content": initial_response}]
        st.session_state.model_name = model_name # Guarda o nome do modelo para uso futuro

# --- Interface do Chat ---
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre os anúncios listados..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analisando..."):
        # MUDANÇA: Chama a nova função para continuar o chat
        updated_history, response_text = send_message_rest(
            api_key=api_key,
            model_name=st.session_state.model_name,
            chat_history=st.session_state.history,
            user_prompt=prompt
        )
        
        # MUDANÇA: Atualiza o histórico na sessão
        st.session_state.history = updated_history
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)