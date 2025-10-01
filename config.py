# config.py
import streamlit as st

def get_gemini_api_key():
    """
    Obtém a chave de API do Gemini a partir dos secrets do Streamlit.
    Se não encontrar, pede ao utilizador para inserir na barra lateral.
    """
    try:
        # Tenta obter a chave do ficheiro secrets.toml
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # Se não encontrar, mostra um campo na barra lateral
        return st.sidebar.text_input("Sua Chave de API Gemini", type="password")