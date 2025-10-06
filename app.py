# app.py
import streamlit as st
import logging

from config import get_gemini_api_key
from services.olx_service import fetch_olx_data
from services.gemini_service import get_available_models, initialize_model, start_chat_session
from app_ui import display_negocios_sidebar, setup_page
# CORREÇÃO: Importa as funções que estavam em falta
from gallery_component import create_gallery
from utils import normalize_data, find_details_for_response

# --- 1. CONFIGURAÇÃO INICIAL ---
setup_page()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# --- 2. SIDEBAR E ENTRADAS DO UTILIZADOR ---
api_key = get_gemini_api_key()
st.sidebar.divider()

jwt_token = st.sidebar.text_input(
    "Seu Token JWT do OLX",
    type="password",
    help="Obtenha este token (Bearer) nas ferramentas de desenvolvedor do seu navegador (F12)."
)
st.sidebar.divider()

selected_model = None
if api_key:
    model_options = get_available_models(api_key)
    if model_options:
        default_model = "gemini-pro-latest"
        try:
            default_index = model_options.index(default_model)
        except ValueError:
            default_index = 0
        selected_model = st.sidebar.selectbox("Escolha o Modelo Gemini", options=model_options, index=default_index)
    else:
        st.sidebar.error("Não foi possível obter os modelos. Verifique a chave de API.")
else:
    st.sidebar.warning("Insira uma chave de API para ver os modelos.")
st.sidebar.divider()

if not api_key or not selected_model or not jwt_token:
    st.info("Por favor, insira a sua chave de API Gemini e o seu Token JWT do OLX para começar.")
    st.stop()

# --- 3. LÓGICA DE OBTENÇÃO DE DADOS ---
dados_brutos = fetch_olx_data(jwt_token, page=st.session_state.page_number)

if not dados_brutos:
    st.warning("Não foi possível obter os dados do OLX. Verifique o seu token.")
    st.stop()

listings_normalizados = normalize_data("OLX", dados_brutos)
display_negocios_sidebar(listings_normalizados)

# --- 4. LÓGICA DO CHAT ---
current_context_id = f"{st.session_state.page_number}"
if "chat" not in st.session_state or st.session_state.get("context_id") != current_context_id:
    st.session_state.context_id = current_context_id
    with st.spinner("A inicializar o assistente com os novos dados..."):
        model = initialize_model(api_key, selected_model)
        chat, initial_response = start_chat_session(model, listings_normalizados)
        st.session_state.chat = chat
        initial_details = find_details_for_response(initial_response, listings_normalizados)
        st.session_state.messages = [{"role": "assistant", "content": initial_response, "details": initial_details}]
        st.rerun()

# --- 5. INTERFACE DO CHAT ---
for i, message in enumerate(st.session_state.get("messages", [])):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "details" in message:
            for j, detail in enumerate(message["details"]):
                images = detail.get("images", [])
                if len(images) > 1:
                    create_gallery(images, key_prefix=f"hist_{i}_{j}")
                elif len(images) == 1:
                    st.image(images[0])
                # if detail.get("url"):
                #     st.link_button("Ver Anúncio ↗️", detail["url"], use_container_width=True, key=f"link_hist_{i}_{j}_{detail['url']}")

if prompt := st.chat_input("Pergunte sobre os anúncios listados..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Analisando..."):
        response = st.session_state.chat.send_message(prompt)
        response_text = response.text
        details = find_details_for_response(response_text, listings_normalizados)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "details": details})
        st.rerun()