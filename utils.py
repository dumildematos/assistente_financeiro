# utils.py
import json
import streamlit as st

def normalize_data(source, raw_data):
    """
    Converte os dados brutos de diferentes fontes para um formato padrão.
    """
    normalized_list = []
    st.write(f"Normalizando dados da fonte: {source}")
    st.write(json.dumps(raw_data, indent=2, ensure_ascii=False))  # Debug: Mostrar dados brutos
    if source == "OLX":
        listings = raw_data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
        for item in listings:
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
                "images": images,
                "videos": [] # Placeholder para vídeos
            })
            
    elif source == "Idealista (Exemplo)":
        listings = raw_data.get("elementList", [])
        for item in listings:
            images = [photo['url'] for photo in item.get('multimedia', []) if photo.get('url')]
            
            normalized_list.append({
                "title": f"{item.get('propertyType', '')} em {item.get('address', '')}",
                "price": f"€ {item.get('price', 0):,}".replace(",", "."),
                "location": item.get('municipality'),
                "url": item.get('url'),
                "images": images,
                "videos": [] # Placeholder para vídeos
            })

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