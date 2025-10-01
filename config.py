# config.py
import streamlit as st
import os # Importar a biblioteca os

def get_gemini_api_key():
    """
    Obtém a chave de API do Gemini a partir das variáveis de ambiente (para Vercel)
    ou dos secrets do Streamlit (para ambiente local).
    """
    # Procura primeiro pela variável de ambiente (usada na Vercel)
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        return api_key

    # Se não encontrar, tenta obter do ficheiro secrets.toml (para teste local)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("Chave de API do Gemini não encontrada. Configure-a nas variáveis de ambiente da Vercel ou no ficheiro secrets.toml local.")
        return None