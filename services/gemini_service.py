# gemini_service.py
import google.generativeai as genai
from prompt import get_initial_prompt

def initialize_model(api_key):
    """
    Configura a API e inicializa o modelo generativo.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-latest')
    return model

def start_chat_session(model, dados_financeiros):
    """
    Inicia uma sessão de chat com o Gemini, envia o prompt inicial e retorna o chat e a primeira resposta.
    """
    initial_prompt = get_initial_prompt(dados_financeiros)
    chat = model.start_chat(history=[])
    response = chat.send_message(initial_prompt)
    return chat, response.text