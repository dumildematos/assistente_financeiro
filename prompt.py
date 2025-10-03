# prompt.py
import json

def get_initial_prompt(normalized_listings):
    """
    Formata e retorna o prompt inicial, recebendo a lista de anúncios já normalizada.
    """
    # Como os dados já estão simplificados, podemos passá-los diretamente para a IA
    return f"""
    Atue como um consultor de negócios e analista de investimentos experiente.
    A sua tarefa é analisar uma lista de anúncios de trespasse e oportunidades de negócio.

    **Regras importantes:**
    1.  **Análise Geral:** Na sua primeira resposta, faça um resumo dos anúncios encontrados, mencionando a variedade de setores e localizações.
    2.  **Análise de Risco:** Encoraje o utilizador a fazer perguntas específicas sobre os pontos fortes, fracos e riscos de cada oportunidade.
    3.  **Seja um Consultor:** Responda a perguntas sobre o potencial de cada negócio e o que deve ser verificado antes de avançar.

    Aqui está a lista de anúncios a serem analisados:
    {json.dumps(normalized_listings, indent=2, ensure_ascii=False)}

    Por favor, comece com a sua análise geral.
    """