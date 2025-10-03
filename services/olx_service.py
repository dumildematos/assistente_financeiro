# olx_service.py
import requests
import streamlit as st
import logging
import jwt

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
        response.raise_for_status()
        token_data = response.json()
        
        # --- MUDANÇA: Descodifica o id_token para obter o nome ---
        id_token = token_data.get("id_token")
        user_name = None
        if id_token:
            try:
                # Descodifica o JWT. A verificação da assinatura é ignorada aqui,
                # pois confiamos na resposta direta e segura (HTTPS) do servidor do OLX.
                decoded_token = jwt.decode(id_token, options={"verify_signature": False})
                user_name = decoded_token.get("name") # O campo do nome pode variar (ex: "name", "given_name")
                logging.info(f"Utilizador autenticado: {user_name}")
            except jwt.exceptions.DecodeError as e:
                logging.error(f"Erro ao descodificar o id_token: {e}")

        # Retorna o dicionário completo do token e o nome do utilizador
        return token_data, user_name
        # --- Fim da Mudança ---

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter o token do OLX: {e.response.text if e.response else e}")
        st.error(f"Erro ao obter o token do OLX. Verifique as credenciais e o redirect_uri.")
        return None, None

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