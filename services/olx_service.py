# olx_service.py
import requests
import streamlit as st
import logging
import jwt


def fetch_olx_data(jwt_token, page=1):
    """
    Faz uma chamada à API GraphQL do OLX usando um token JWT fornecido manualmente.
    """
    endpoint_url = "https://www.olx.pt/apigateway/graphql"
    
    limit = 50
    offset = (page - 1) * limit

    search_params = [
        {"key": "offset", "value": str(offset)},
        {"key": "limit", "value": str(limit)},
        {"key": "query", "value": "trespasse negocio"},
        {"key": "category_id", "value": "4787"}
    ]

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
    variables = {"searchParameters": search_params}
    
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
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
        logging.error(f"Erro ao contactar a API GraphQL: {e}")
        st.error("Erro ao obter dados do OLX. Verifique se o seu token JWT é válido e não expirou.")
        return None