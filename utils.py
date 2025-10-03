# utils.py
import json
import streamlit as st

def normalize_data(source, raw_data):
    """
    Converts raw data from different sources into a standard format.
    Now handles 'null' responses from the API.
    """
    normalized_list = []
    
    if source == "OLX":
        # --- MUDANÇA: Adiciona uma verificação de segurança ---
        client_listings = raw_data.get("data", {}).get("clientCompatibleListings")
        
        # Só prossegue se 'client_listings' não for None
        if client_listings:
            listings = client_listings.get("data", [])
            for item in listings:
                # ... (o resto da lógica de normalização não muda)
                price_label = "A consultar"
                for param in item.get("params", []):
                    if param.get("key") == "price":
                        price_label = param.get("value", {}).get("label", "A consultar")
                        break
                
                images = []
                for photo in item.get("photos", []):
                    link = photo.get("link")
                    if link:
                        images.append(link.replace("{width}x{height}", "400x300"))
                
                normalized_list.append({
                    "title": item.get("title"),
                    "price": price_label,
                    "location": item.get("location", {}).get("city", {}).get("name"),
                    "url": item.get("url"),
                    "images": images
                })
        else:
            # Mostra o erro da API na interface do Streamlit
            api_errors = raw_data.get("errors")
            if api_errors:
                st.error(f"A API do OLX retornou um erro: {api_errors[0]['message']}")

    # ... (lógica para outras fontes)

    return normalized_list
def find_details_for_response(response_text, normalized_listings):
    """
    Verifica o texto de resposta para nomes de negócios e retorna os detalhes
    a partir da lista de anúncios JÁ NORMALIZADA.
    """
    details_found = []
    for listing in normalized_listings:
        title = listing.get("title")
        if title and title.lower() in response_text.lower():
            # Como a 'listing' já é o nosso formato simplificado, podemos usá-la diretamente
            details_found.append(listing)
    return details_found