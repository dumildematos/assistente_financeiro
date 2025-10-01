# gemini_service.py
import requests
import streamlit as st
from prompt import get_initial_prompt

def start_chat_session(api_key, model_name, dados):
    """
    Inicia uma conversa com a API REST do Gemini e retorna a primeira resposta e o histórico.
    """
    initial_prompt = get_initial_prompt(dados)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"role": "user", "parts": [{"text": initial_prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        initial_response_text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Cria o histórico inicial da conversa
        chat_history = [
            {"role": "user", "parts": [{"text": initial_prompt}]},
            {"role": "assistant", "parts": [{"text": initial_response_text}]}
        ]
        return chat_history, initial_response_text
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao contactar a API do Gemini: {e}")
        return None, None

def send_message_rest(api_key, model_name, chat_history, user_prompt):
    """
    Envia uma nova mensagem do utilizador, juntamente com o histórico, para a API REST.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Adiciona a nova mensagem do utilizador ao histórico
    chat_history.append({"role": "user", "parts": [{"text": user_prompt}]})
    
    # O payload agora contém o histórico completo
    payload = {"contents": chat_history}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        assistant_response_text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Adiciona a resposta do assistente ao histórico
        chat_history.append({"role": "assistant", "parts": [{"text": assistant_response_text}]})
        
        return chat_history, assistant_response_text
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao contactar a API do Gemini: {e}")
        return chat_history, "Ocorreu um erro ao processar o seu pedido."