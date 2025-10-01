# app.py
import streamlit as st
from config import get_gemini_api_key
from services.olx_service import fetch_olx_data
from services.gemini_service import get_available_models, initialize_model, start_chat_session
from app_ui import display_negocios_sidebar, setup_page
from streamlit_modal import Modal
from gallery_component import create_gallery # MUDANÇA: Importa o novo componente

def find_details_for_response(response_text, all_data):
    """
    Verifica o texto de resposta para nomes de negócios e retorna os detalhes
    relevantes (URL do anúncio, TODAS as imagens, vídeos) dos negócios correspondentes.
    """
    details_found = []
    listings = all_data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
    
    for listing in listings:
        title = listing.get("title")
        if title and title.lower() in response_text.lower():
            details = {"url": listing.get("url"), "images": [], "videos": []}
            
            # --- MUDANÇA: Percorre todas as fotos em vez de apenas a primeira ---
            images = []
            for photo in listing.get("photos", []):
                raw_link = photo.get("link")
                if raw_link:
                    image_url = raw_link.replace("{width}x{height}", "400x300")
                    images.append(image_url)
            details["images"] = images
            # --- Fim da Mudança ---

            # Lógica para vídeos (preparado para o futuro)
            videos = []
            if listing.get("videos"):
                for video in listing["videos"]:
                    if video.get("link"):
                        videos.append(video.get("link"))
            details["videos"] = videos

            details_found.append(details)
                    
    return details_found

# --- O resto do ficheiro é exatamente o mesmo ---

# Configuração da Página e Avisos
setup_page()

# Inicializa o estado da página
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# Obter Chaves, Tokens e Modelo
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

# Carregar Dados e Mostrar Sidebar
dados = fetch_olx_data(bearer_token, page=st.session_state.page_number)
if dados:
    display_negocios_sidebar(dados)
else:
    st.warning("Não foi possível obter os dados do OLX. Verifique o token e tente novamente.")
    st.stop()

# Inicialização do Chat
if "chat" not in st.session_state:
    with st.spinner("A inicializar o assistente..."):
        model = initialize_model(api_key, selected_model)
        chat, initial_response = start_chat_session(model, dados)
        st.session_state.chat = chat
        st.session_state.messages = [{"role": "assistant", "content": initial_response, "details": find_details_for_response(initial_response, dados)}]

# Loop para exibir o histórico de mensagens
for i, message in enumerate(st.session_state.get("messages", [])):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "details" in message:
            for j, detail in enumerate(message["details"]):
                images = detail.get("images", [])
                
                # Se houver mais de uma imagem, usa o componente de galeria
                if len(images) > 1:
                    create_gallery(images, key_prefix=f"hist_{i}_{j}")
                # Se houver apenas uma imagem, mostra-a normalmente
                elif len(images) == 1:
                    st.image(images[0])
                
                for video_url in detail.get("videos", []): st.video(video_url)
                # if detail.get("url"):
                #     st.link_button("Ver Anúncio no OLX ↗️", detail["url"], use_container_width=True, key=f"link_hist_{i}_{j}_{detail['url']}")


# Loop para novas mensagens do utilizador
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
                images = detail.get("images", [])

                if len(images) > 1:
                    create_gallery(images, key_prefix=f"new_{k}")
                elif len(images) == 1:
                    st.image(images[0])
                
                for video_url in detail.get("videos", []): st.video(video_url)
                # if detail.get("url"):
                #     st.link_button("Ver Anúncio no OLX ↗️", detail["url"], use_container_width=True, key=f"link_new_{k}_{detail['url']}")