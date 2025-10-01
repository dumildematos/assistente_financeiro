# olx_service.py
import requests
import streamlit as st

# MUDANÇA: A função agora aceita um número de página
def fetch_olx_data(bearer_token, page=1):
    """
    Faz uma chamada à API GraphQL do OLX para obter os dados dos anúncios.
    Agora suporta paginação.
    """
    endpoint_url = "https://www.olx.pt/apigateway/graphql"

    # MUDANÇA: Define o limite e calcula o offset
    limit = 50
    offset = (page - 1) * limit

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

    # MUDANÇA: Atualiza os valores de 'limit' e 'offset' no payload
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
        "Content-Type": "application/json"
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
        st.error(f"Erro ao contactar a API do OLX: {e}")
        st.error("Verifique se o seu Bearer Token é válido e não expirou.")
        return None