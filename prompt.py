# prompt.py
import json


def get_initial_prompt(dados):
    """
    Navega na estrutura complexa do JSON, extrai os dados essenciais dos anúncios
    e formata um prompt limpo para a IA.
    """
    # Navega de forma segura até à lista de anúncios
    listings = dados.get("data", {}).get("clientCompatibleListings", {}).get("data", [])

    simplified_listings = []
    for listing in listings:
        # Extrai o preço do campo 'params'
        price_label = "Preço a consultar"
        for param in listing.get("params", []):
            if param.get("key") == "price":
                price_label = param.get("value", {}).get("label", "Preço a consultar")
                break

        # Cria uma versão simplificada de cada anúncio
        simplified_listing = {
            "id": listing.get("id"),
            "titulo": listing.get("title"),
            "preco": price_label,
            "localizacao": listing.get("location", {}).get("city", {}).get("name"),
            "descricao": listing.get("description"),
            "url": listing.get("url")
        }
        simplified_listings.append(simplified_listing)

    # O prompt que será enviado para a IA
    return f"""
    Atue como um consultor de negócios e analista de investimentos experiente.
    A sua tarefa é analisar uma lista de anúncios de trespasse e oportunidades de negócio, fornecida em formato JSON simplificado.

    **Regras importantes:**
    1.  **Análise Geral:** Na sua primeira resposta, faça um resumo do(s) anúncio(s) encontrado(s), mencionando o tipo de negócio e a localização.
    2.  **Análise de Risco:** Encoraje o utilizador a fazer perguntas específicas sobre os pontos fortes, fracos e riscos potenciais de cada oportunidade.
    3.  **Seja um Consultor:** Responda a perguntas sobre o potencial de cada negócio, o que deve ser verificado antes de avançar (due diligence), e como o negócio se compara com outros.

    Aqui está a lista de anúncios a serem analisados:
    {json.dumps(simplified_listings, indent=2)}

    Por favor, comece com a sua análise geral.
    """