# app_ui.py
import streamlit as st


def setup_page():
    st.set_page_config(page_title="Gemini Business Advisor", page_icon="📈")
    st.title("📈 Assistente de Negócios com Gemini")
    st.caption("Analisa oportunidades de negócio em tempo real e ajuda a identificar riscos e potenciais.")
    st.warning(
        "**Aviso Legal:** As análises são geradas por IA. Conduza a sua própria due diligence antes de qualquer investimento.",
        icon="⚠️"
    )


def display_negocios_sidebar(dados):
    st.sidebar.header("Anúncios Encontrados")
    listings = dados.get("data", {}).get("clientCompatibleListings", {}).get("data", [])

    if not listings:
        st.sidebar.write("Nenhum anúncio encontrado com os critérios atuais.")
        return

    for listing in listings:
        with st.sidebar.container():
            image_url = None
            if listing.get("photos"):
                raw_link = listing["photos"][0].get("link")
                if raw_link:
                    image_url = raw_link.replace("{width}x{height}", "400x300")

            if image_url:
                st.image(image_url)

            title = listing.get("title", "Título indisponível")
            st.subheader(title)

            price_label = "Preço a consultar"
            for param in listing.get("params", []):
                if param.get("key") == "price":
                    price_label = param.get("value", {}).get("label", "Preço a consultar")
                    break

            st.write(f"**Preço:** {price_label}")

            location = listing.get("location", {}).get("city", {}).get("name", "N/A")
            st.write(f"**Local:** {location}")

            st.divider()