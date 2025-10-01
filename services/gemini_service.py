# gemini_service.py
from prompt import get_initial_prompt
import google.generativeai as genai
import streamlit as st

def get_available_models(api_key):
    """
    Lista os modelos generativos disponíveis que suportam 'generateContent'.
    Retorna uma lista de nomes de modelos simplificados (ex: 'gemini-1.5-pro-latest').
    """
    try:
        genai.configure(api_key=api_key)
        model_list = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Extrai o nome limpo do modelo, removendo o prefixo "models/"
                model_list.append(m.name.split('/')[-1])
        return model_list
    except Exception as e:
        st.error(f"Não foi possível obter a lista de modelos: {e}")
        return []

def initialize_model(api_key, model_name):
    """
    Configures the API and initializes the generative model.
    """
    genai.configure(api_key=api_key)
    # Adiciona o prefixo "models/" de volta, que é necessário para a API
    model = genai.GenerativeModel(f"models/{model_name}")
    return model

def start_chat_session(model, dados):
    """
    Starts a chat session with the Gemini model and sends the initial prompt.
    """
    initial_prompt = get_initial_prompt(dados)
    chat = model.start_chat(history=[])
    response = chat.send_message(initial_prompt)
    return chat, response.text