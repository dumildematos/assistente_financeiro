# olx_service.py
import requests
import streamlit as st

def fetch_olx_data(bearer_token):
    """
    Faz uma chamada à API GraphQL do OLX para obter os dados dos anúncios.
    """
    endpoint_url = "https://www.olx.pt/apigateway/graphql"

    query = """
    query ListingSearchQuery($searchParameters: [SearchParameter!]!) {
      clientCompatibleListings(searchParameters: $searchParameters) {
        __typename
        ... on ListingSuccess {
          data {
            id
            title
            description
            url
            location { city { name } }
            photos { link }
            params {
              key
              value {
                __typename
                ... on PriceParam { label }
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "searchParameters": [
            {"key": "offset", "value": "0"},
            {"key": "limit", "value": "20"},
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
        response.raise_for_status()  # Lança um erro para respostas HTTP > 400
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao contactar a API do OLX: {e}")
        st.error("Verifique se o seu Bearer Token é válido e não expirou.")
        return None