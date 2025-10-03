# idealista_service.py
import streamlit as st

def fetch_idealista_data():
    """
    Função de exemplo que simula uma chamada à API do Idealista.
    No futuro, esta função conteria a lógica real para obter os dados.
    """
    st.info("A usar dados de exemplo para o Idealista.", icon="ℹ️")
    
    # Exemplo de estrutura de dados que a API do Idealista poderia retornar
    return {
        "elementList": [
            {
                "propertyCode": 30865329,
                "thumbnail": "https://img3.idealista.pt/blur/WEB_340-L/0/id.pro.es.image.master/7a/74/59/1107567705.jpg",
                "price": 650000,
                "propertyType": "moradia",
                "operation": "venda",
                "size": 357,
                "exterior": True,
                "rooms": 4,
                "address": "Foros de Amora, Amora",
                "province": "Setúbal",
                "municipality": "Seixal",
                "url": "https://www.idealista.pt/imovel/30865329/",
                "multimedia": [
                    {"url": "https://img3.idealista.pt/blur/WEB_DETAIL-L/0/id.pro.es.image.master/7a/74/59/1107567705.jpg"},
                    {"url": "https://img3.idealista.pt/blur/WEB_DETAIL-L/0/id.pro.es.image.master/b4/d9/85/1107567708.jpg"},
                    {"url": "https://img3.idealista.pt/blur/WEB_DETAIL-L/0/id.pro.es.image.master/5f/cc/a2/1107567713.jpg"}
                ]
            },
            {
                "propertyCode": 33458626,
                "thumbnail": "https://img3.idealista.pt/blur/WEB_340-L/0/id.pro.pt.image.master/68/d8/50/1105936742.jpg",
                "price": 120000,
                "propertyType": "loja",
                "operation": "trespasse",
                "size": 60,
                "exterior": True,
                "rooms": 2,
                "address": "Baixa, Faro",
                "province": "Faro",
                "municipality": "Faro",
                "url": "https://www.idealista.pt/imovel/33458626/",
                "multimedia": [
                    {"url": "https://img3.idealista.pt/blur/WEB_DETAIL-L/0/id.pro.pt.image.master/68/d8/50/1105936742.jpg"}
                ]
            }
        ]
    }