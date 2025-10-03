# app_ui.py
import streamlit as st

def setup_page():
    st.set_page_config(page_title="Gemini Business Advisor", page_icon="📈")
    st.title("📈 Assistente de Negócios com Gemini")
    st.caption("Analisa oportunidades de negócio em tempo real e ajuda a identificar riscos e potenciais.")
    st.warning(
        "**Aviso Legal:** As análises são geradas por IA. Conduza a sua própria due diligence antes de qualquer investimento.", icon="⚠️"
    )

def display_negocios_sidebar(normalized_listings):
    num_listings = len(normalized_listings)
    st.sidebar.header(f"Anúncios Encontrados ({num_listings})")

    if not normalized_listings:
        st.sidebar.warning("Nenhum anúncio encontrado com os filtros atuais.")
    else:
        #...(código para exibir a lista de anúncios inalterado)...
        for idx, listing in enumerate(normalized_listings, start=1):
            with st.sidebar.container():
                if listing.get("images"):
                    st.image(listing["images"][0])
                st.subheader(f"{idx}. {listing.get('title', 'N/A')}")
                st.write(f"**Preço:** {listing.get('price', 'N/A')}")
                st.write(f"**Local:** {listing.get('location', 'N/A')}")
                st.divider()

    # --- MUDANÇA: Botões de Paginação agora são condicionais ---
    # Só mostra os botões se a sessão atual tiver apenas a fonte OLX selecionada
    if st.session_state.get("only_olx_selected", False):
        st.sidebar.divider()
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.page_number <= 1)):
                st.session_state.page_number -= 1
                st.rerun()
        with col2:
            # Desativa o botão 'Próxima' se a página atual tiver menos de 50 resultados
            if st.button("Próxima ➡️", use_container_width=True, disabled=(num_listings < 50)):
                st.session_state.page_number += 1
                st.rerun()
        st.sidebar.write(f"Página: **{st.session_state.page_number}**")
