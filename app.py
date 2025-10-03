# app.py
import streamlit as st
import logging
import secrets

from config import get_gemini_api_key
from services.olx_service import get_olx_token, fetch_olx_data
from services.idealista_service import fetch_idealista_data
from services.gemini_service import get_available_models, initialize_model, start_chat_session
from app_ui import display_negocios_sidebar, setup_page
from gallery_component import create_gallery
from utils import normalize_data, find_details_for_response

# --- CONFIGURAÇÃO DOS LOGS ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

# --- 1. CONFIGURAÇÃO DA PÁGINA E ESTADO DA SESSÃO ---
setup_page()
if "page_number" not in st.session_state: st.session_state.page_number = 1
if "olx_token" not in st.session_state: st.session_state.olx_token = None
if "oauth_state" not in st.session_state: st.session_state.oauth_state = None
if "user_name" not in st.session_state: st.session_state.user_name = None

# --- 2. SIDEBAR E ENTRADAS DO UTILIZADOR ---
api_key = get_gemini_api_key()

# Painel de autenticação e boas-vindas na sidebar
with st.sidebar:
    st.divider()
    if st.session_state.user_name:
        st.success(f"Autenticado como: **{st.session_state.user_name}**")
        if st.button("Logout do OLX", use_container_width=True):
            st.session_state.olx_token = None
            st.session_state.user_name = None
            st.query_params.clear()
            st.rerun()
    st.divider()
    
    st.subheader("Fontes dos Anúncios")
    use_olx = st.checkbox("OLX", value=True)
    use_idealista = st.checkbox("Idealista (Exemplo)")
    st.session_state.only_olx_selected = use_olx and not use_idealista
    
    selected_model = None
    if api_key:
        model_options = get_available_models(api_key)
        if model_options:
            default_model = "gemini-pro-latest"
            try:
                default_index = model_options.index(default_model)
            except ValueError:
                default_index = 0
            selected_model = st.selectbox("Escolha o Modelo Gemini", options=model_options, index=default_index)
        else:
            st.error("Não foi possível obter os modelos.")
    else:
        st.warning("Insira uma chave de API para ver os modelos.")
    st.divider()

if not api_key or not selected_model:
    st.info("Por favor, insira a sua chave de API Gemini e escolha um modelo para começar.")
    st.stop()

# --- 3. LÓGICA DE AUTENTICAÇÃO E OBTENÇÃO DE DADOS ---
listings_normalizados = []
dados_carregados = False

# Lógica para o Idealista (não requer autenticação)
if use_idealista:
    idealista_raw_data = fetch_idealista_data()
    if idealista_raw_data:
        idealista_listings = normalize_data("Idealista (Exemplo)", idealista_raw_data)
        listings_normalizados.extend(idealista_listings)
    dados_carregados = True

# Lógica para o OLX (requer autenticação OAuth 2.0)
if use_olx:
    try:
        CLIENT_ID = st.secrets["OLX_CLIENT_ID"]
        CLIENT_SECRET = st.secrets["OLX_CLIENT_SECRET"]
    except KeyError:
        st.error("Credenciais do OLX (CLIENT_ID, CLIENT_SECRET) não encontradas no secrets.toml.")
        st.stop()

    AUTHORIZE_URL = "https://www.olx.pt/oauth/authorize"
    REDIRECT_URI = st.get_option("server.baseUrlPath").strip('/')

    if st.session_state.olx_token:
        access_token = st.session_state.olx_token.get('access_token')
        dados_brutos = fetch_olx_data(access_token, page=st.session_state.page_number)
        if dados_brutos:
            olx_listings = normalize_data("OLX", dados_brutos)
            listings_normalizados.extend(olx_listings)
            dados_carregados = True
        elif not use_idealista: # Só mostra o aviso se não houver outros dados
            st.warning("Não foi possível obter os dados do OLX. O seu token pode ter expirado.")
            # O botão de logout já está permanentemente visível na sidebar
    else:
        auth_code = st.query_params.get("code")
        received_state = st.query_params.get("state")
        if auth_code:
            if not received_state or received_state != st.session_state.get("oauth_state"):
                st.error("Erro de segurança: o 'state' da autenticação não corresponde. Tente novamente.")
                st.stop()
            
            with st.spinner("A finalizar autenticação..."):
                token_data, user_name = get_olx_token(CLIENT_ID, CLIENT_SECRET, auth_code, REDIRECT_URI)
                if token_data:
                    st.session_state.olx_token = token_data
                    st.session_state.user_name = user_name
                    st.session_state.oauth_state = None
                    st.query_params.clear()
                    st.rerun()
        else:
            st.session_state.oauth_state = secrets.token_hex(16)
            auth_url = f"{AUTHORIZE_URL}?response_type=code&client_id={CLIENT_ID}&scope=v2%20read%20write&redirect_uri={REDIRECT_URI}&state={st.session_state.oauth_state}"
            if not st.session_state.user_name: # Mostra o botão apenas se não estiver logado
                st.sidebar.link_button("Autorizar com OLX 🔒", auth_url, use_container_width=True)
            if not use_idealista:
                st.info("A fonte OLX requer autorização. Por favor, clique no botão na barra lateral.")
                st.stop()
            
# --- 4. EXIBIÇÃO E LÓGICA DO CHAT ---
if not listings_normalizados and not dados_carregados:
    st.stop()

display_negocios_sidebar(listings_normalizados)

current_context_id = f"{use_olx}-{use_idealista}-{st.session_state.page_number}"
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
                if detail.get("url"):
                    st.link_button("Ver Anúncio ↗️", detail["url"], use_container_width=True, key=f"link_hist_{i}_{j}_{detail['url']}")

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