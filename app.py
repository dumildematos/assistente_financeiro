# app.py
import streamlit as st
from config import get_gemini_api_key
from services.olx_service import fetch_olx_data
from services.gemini_service import get_available_models, initialize_model, start_chat_session
from app_ui import display_negocios_sidebar, setup_page

# A função 'find_details_for_response' não precisa de alterações
def find_details_for_response(response_text, all_data):
    # ... (código inalterado)
    details_found = []
    listings = all_data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
    for listing in listings:
        title = listing.get("title")
        if title and title.lower() in response_text.lower():
            details = {"url": listing.get("url"), "images": [], "videos": []}
            if listing.get("photos"):
                raw_link = listing["photos"][0].get("link")
                if raw_link:
                    details["images"].append(raw_link.replace("{width}x{height}", "400x300"))
            details_found.append(details)
    return details_found

setup_page()

if "page_number" not in st.session_state:
    st.session_state.page_number = 1

api_key = get_gemini_api_key()
bearer_token = st.sidebar.text_input("Seu Bearer Token do OLX", type="password")
st.sidebar.divider()

if api_key:
    model_options = get_available_models(api_key)
    default_model = "gemini-pro-latest"
    try:
        default_index = model_options.index(default_model)
    except ValueError:
        default_index = 0
    selected_model = st.sidebar.selectbox("Escolha o Modelo Gemini", options=model_options, index=default_index)
else:
    selected_model = None
st.sidebar.divider()

if not api_key or not bearer_token:
    st.info("Por favor, insira a sua chave de API Gemini e o seu Bearer Token do OLX para começar.")
    st.stop()
    
if not selected_model:
    st.error("Nenhum modelo selecionado. Verifique a sua chave de API.")
    st.stop()

dados = fetch_olx_data(bearer_token, page=st.session_state.page_number)
if dados:
    display_negocios_sidebar(dados)
else:
    st.warning("Não foi possível obter os dados do OLX. Verifique o token e tente novamente.")
    st.stop()

if "chat" not in st.session_state:
    with st.spinner("A inicializar o assistente..."):
        model = initialize_model(api_key, selected_model)
        chat, initial_response = start_chat_session(model, dados)
        st.session_state.chat = chat
        st.session_state.messages = [{"role": "assistant", "content": initial_response, "details": find_details_for_response(initial_response, dados)}]

# --- Interface do Chat ---
for i, message in enumerate(st.session_state.get("messages", [])):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "details" in message:
            for j, detail in enumerate(message["details"]):
                for img_url in detail.get("images", []):
                    st.image(img_url)
                for video_url in detail.get("videos", []):
                    st.video(video_url)
                
                # MUDANÇA: Adiciona um 'if' para verificar se o URL existe
                if detail.get("url"):
                    st.link_button("Ver Anúncio no OLX ↗️", detail["url"], use_container_width=True, key=f"hist_{i}_{j}_{detail['url']}")

if prompt := st.chat_input("Pergunte sobre os anúncios listados..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analisando..."):
        response = st.session_state.chat.send_message(prompt)
        response_text = response.text
        details = find_details_for_response(response_text, dados)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "details": details})
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
            for k, detail in enumerate(details):
                for img_url in detail.get("images", []):
                    st.image(img_url)
                for video_url in detail.get("videos", []):
                    st.video(video_url)
                
                # MUDANÇA: Adiciona um 'if' para verificar se o URL existe
                if detail.get("url"):
                    st.link_button("Ver Anúncio no OLX ↗️", detail["url"], use_container_width=True, key=f"new_{k}_{detail['url']}")