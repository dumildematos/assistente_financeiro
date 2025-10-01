import json
import streamlit as st

def carregar_dados_financeiros(nome_ficheiro='negocios.json'):
    """
    Carrega os dados financeiros de um ficheiro JSON.
    """
    try:
        # Certifique-se de que encoding='utf-8' está aqui
        with open(nome_ficheiro, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro '{nome_ficheiro}' não foi encontrado.")
        return None
    except Exception as e:
        # Este erro pode apanhar o UnicodeEncodeError se o ficheiro foi guardado com o formato errado
        st.error(f"Erro ao ler o ficheiro JSON: {e}")
        return None