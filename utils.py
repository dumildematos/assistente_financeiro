# utils.py
import json
import streamlit as st

def carregar_dados_financeiros(nome_ficheiro='negocios.json'):
    """
    Carrega os dados financeiros de um ficheiro JSON.
    """
    try:
        with open(nome_ficheiro, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro '{nome_ficheiro}' não foi encontrado. Certifique-se que ele está na mesma pasta.")
        return None