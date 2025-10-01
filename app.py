# app.py
import streamlit as st
from config import get_gemini_api_key
from services.olx_service import fetch_olx_data
from services.gemini_service import initialize_model, start_chat_session
from app_ui import display_negocios_sidebar, setup_page

# --- Configuração da Página e Avisos ---
setup_page()

# --- Obter Chaves e Tokens ---
api_key = get_gemini_api_key()
# Este campo de texto é a chave para a versão dinâmica
bearer_token = st.sidebar.text_input("Seu Bearer Token do OLX", type="password", help="Obtenha este token nas ferramentas de desenvolvedor do seu navegador (F12).")

# A aplicação irá esperar aqui até que ambas as chaves sejam fornecidas
if not api_key or not bearer_token:
    st.info("Por favor, insira a sua chave de API Gemini e o seu Bearer Token do OLX para começar.")
    st.stop()

# --- Carregar Dados da API e Mostrar Sidebar ---
# Usa o token fornecido para buscar os dados em tempo real
dados = fetch_olx_data(bearer_token)
if dados:
    display_negocios_sidebar(dados)
else:
    # Se fetch_olx_data retornar None (devido a um erro), a app para aqui.
    st.warning("Não foi possível obter os dados do OLX. Verifique o token e tente novamente.")
    st.stop()

# --- Inicialização e Interface do Chat (sem alterações) ---
if "chat" not in st.session_state:
    with st.spinner("A inicializar o assistente..."):
        model = initialize_model(api_key)
        chat, initial_response = start_chat_session(model, dados)
        st.session_state.chat = chat
        st.session_state.messages = [{"role": "assistant", "content": initial_response}]

for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre os anúncios listados..."):
    # (O resto do código não muda)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analisando..."):
        response = st.session_state.chat.send_message(prompt)
        response_text = response.text
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)