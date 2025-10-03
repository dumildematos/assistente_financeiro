# olx_service.py
import requests
import streamlit as st
import logging

def get_olx_token(client_id, client_secret, code, redirect_uri):
    """
    Troca o código de autorização por um access token, usando o fluxo authorization_code.
    """
    token_url = "https://www.olx.pt/api/open/oauth/token"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "v2 read write",
        "code": code,
        "redirect_uri": redirect_uri
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "version": "2.0",
        "Accept": "application/json"
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        
        # MUDANÇA: Adiciona um log para ver a resposta do servidor em caso de erro
        if response.status_code != 200:
            logging.error(f"OLX token request failed with status {response.status_code}.")
            logging.error(f"Server response: {response.text}")
            
        response.raise_for_status() # Esta linha irá causar o erro se o status não for 2xx
        
        logging.info("Token do OLX obtido com sucesso via OAuth 2.0.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter o token do OLX: {e.response.text if e.response else e}")
        st.error(f"Erro ao obter o token do OLX. Verifique as credenciais e o redirect_uri.")
        return None
def authenticate_olx_client(client_id, client_secret):
    """
    Autentica a aplicação usando o grant_type 'client_credentials'
    e retorna o access token.
    """
    token_url = "https://www.olx.pt/api/open/oauth/token"
    
    # O payload é enviado como 'form-urlencoded'
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "v2 read write"
    }
    
    headers = {
        # Como especificado pela documentação para este tipo de pedido
        "Content-Type": "application/x-www-form-urlencoded",
        "version": "2.0",
        "Accept": "application/json"
    }

    try:
        # Usa o parâmetro 'data' para enviar como 'x-www-form-urlencoded'
        response = requests.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        st.write(f"Token Data: {token_data}")  # Debug: Mostrar os dados do token
        return token_data.get("access_token") # Retorna apenas o token de acesso
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na autenticação com o OLX: {e}")
        st.error("Verifique se o seu Client ID e Client Secret estão corretos no secrets.toml.")
        return None

def fetch_olx_data(access_token, page=1):
    """
    Faz uma chamada à API GraphQL do OLX para obter os dados dos anúncios,
    usando o access token obtido.
    """
    endpoint_url = "https://www.olx.pt/apigateway/graphql"
    
    limit = 50
    offset = (page - 1) * limit
    bearer_token = f"Bearer {access_token}"

    query = """
    query ListingSearchQuery($searchParameters: [SearchParameter!]!) {
      clientCompatibleListings(searchParameters: $searchParameters) {
        __typename
        ... on ListingSuccess {
          data { id, title, description, url, location { city { name } }, photos { link }, params { key, value { __typename, ... on PriceParam { label } } } }
        }
      }
    }
    """

    variables = {
        "searchParameters": [
            {"key": "offset", "value": str(offset)},
            {"key": "limit", "value": str(limit)},
            {"key": "query", "value": "trespasse negocio"},
            {"key": "category_id", "value": "4787"}
        ]
    }

    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/json",
        "version": "2.0",
        "Accept": "*/*"
    }

    try:
        response = requests.post(
            endpoint_url,
            json={"query": query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter os dados do OLX: {e}")
        return None