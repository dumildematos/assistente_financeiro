# app_ui.py
import streamlit as st

def setup_page():
    st.set_page_config(page_title="Gemini Business Advisor", page_icon="📈")
    st.title("📈 Assistente de Negócios com Gemini")
    st.caption("Analisa oportunidades de negócio em tempo real e ajuda a identificar riscos e potenciais.")
    st.warning(
        "**Aviso Legal:** As análises são geradas por IA. Conduza a sua própria due diligence antes de qualquer investimento.", icon="⚠️"
    )

def display_negocios_sidebar(dados):
    listings = dados.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
    
    # MUDANÇA: Obtém a quantidade de anúncios encontrados
    num_listings = len(listings)
    
    # MUDANÇA: Atualiza o cabeçalho para incluir a contagem
    st.sidebar.header(f"Anúncios Encontrados ({num_listings})")

    if not listings:
        st.sidebar.warning("Nenhum anúncio encontrado nesta página.")
    else:
        # MUDANÇA: Usa enumerate para obter um contador (idx)
        # O 'start=1' faz com que a contagem comece em 1 em vez de 0
        for idx, listing in enumerate(listings, start=1):
            with st.sidebar.container():
                image_url = None
                if listing.get("photos"):
                    raw_link = listing["photos"][0].get("link")
                    if raw_link:
                        image_url = raw_link.replace("{width}x{height}", "400x300")
                if image_url:
                    st.image(image_url)
                
                title = listing.get("title", "Título indisponível")
                # MUDANÇA: Adiciona o número ao título do anúncio
                st.subheader(f"{idx}. {title}")
                
                price_label = "Preço a consultar"
                for param in listing.get("params", []):
                    if param.get("key") == "price":
                        price_label = param.get("value", {}).get("label", "Preço a consultar")
                        break
                st.write(f"**Preço:** {price_label}")
                
                location = listing.get("location", {}).get("city", {}).get("name", "N/A")
                st.write(f"**Local:** {location}")
                
                st.divider()

    # --- Botões de Paginação (código inalterado) ---
    st.sidebar.divider()
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.page_number <= 1)):
            st.session_state.page_number -= 1
            st.rerun()
    with col2:
        if st.button("Próxima ➡️", use_container_width=True, disabled=(not listings)):
            st.session_state.page_number += 1
            st.rerun()
    st.sidebar.write(f"Página: **{st.session_state.page_number}**")