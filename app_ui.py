# app_ui.py
import streamlit as st

def setup_page():
    st.set_page_config(page_title="Gemini Business Advisor", page_icon="📈")
    st.title("📈 Assistente de Negócios com Gemini")
    st.caption("Analisa oportunidades de negócio e ajuda a identificar riscos e potenciais.")
    st.warning(
        "**Aviso Legal:** As análises são geradas por IA. Conduza a sua própria due diligence antes de qualquer investimento.", icon="⚠️"
    )

def display_negocios_sidebar(normalized_listings):
    num_listings = len(normalized_listings)
    st.sidebar.header(f"Anúncios Encontrados ({num_listings})")

    if not normalized_listings:
        st.sidebar.warning("Nenhum anúncio encontrado nesta página.")
    else:
        for idx, listing in enumerate(normalized_listings, start=1):
            with st.sidebar.container():
                if listing.get("images"):
                    st.image(listing["images"][0])
                
                st.subheader(f"{idx}. {listing.get('title', 'N/A')}")
                st.write(f"**Preço:** {listing.get('price', 'N/A')}")
                st.write(f"**Local:** {listing.get('location', 'N/A')}")
                st.divider()

    # --- NOVO: Controlos de Paginação ---
    st.sidebar.divider()
    st.sidebar.subheader("Paginação")
    
    # Cria duas colunas para os botões
    col1, col2 = st.sidebar.columns(2)

    with col1:
        # Botão Anterior: só é clicável se não estivermos na primeira página
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.page_number <= 1)):
            st.session_state.page_number -= 1
            st.rerun() # Força a reaplicação do script com o novo número de página

    with col2:
        # Botão Próxima: é desativado se a página atual não tiver 50 anúncios (indicando que é a última)
        if st.button("Próxima ➡️", use_container_width=True, disabled=(num_listings < 50)):
            st.session_state.page_number += 1
            st.rerun() # Força a reaplicação do script com o novo número de página
    
    st.sidebar.write(f"Página: **{st.session_state.page_number}**")