
📈 Assistente de Análise de Negócios com Gemini e Streamlit
Uma aplicação web interativa que utiliza a API do Google Gemini para atuar como um assistente de negócios, analisando anúncios de oportunidades de investimento em tempo real. A interface é construída com Streamlit e o projeto está estruturado para ser modular, escalável e pronto para deploy.

(Lembre-se de substituir o link acima pelo URL do seu repositório no GitHub)

(Recomendo tirar um screenshot da sua aplicação a funcionar e colocar o link aqui)

✨ Funcionalidades Principais
Interface de Chat Interativa: Construída com Streamlit para uma experiência de utilizador fluida e moderna.

Análise por IA: Integração com a API do Google Gemini para fornecer análises inteligentes sobre oportunidades de negócio.

Dados em Tempo Real: Recolhe e analisa dados ao vivo de fontes externas (atualmente configurado para uma API GraphQL do OLX).

Visualização de Dados: Exibe os anúncios encontrados numa barra lateral organizada, com imagens, preços e localizações.

Estrutura Modular: O código é dividido em módulos para UI, serviços de API e configuração, facilitando a manutenção e expansão.

Pronto para Deploy: Inclui configuração para deploy na Vercel, com gestão segura de chaves de API através de variáveis de ambiente.

🛠️ Tecnologias Utilizadas
Backend: Python 3.9+

Inteligência Artificial: Google Gemini API (google-generativeai)

Interface Web: Streamlit

Requisições HTTP: Requests

Manipulação de Dados: Pandas

Deploy: Vercel

📂 Estrutura do Projeto
O projeto é organizado de forma modular para separar as responsabilidades:

assistente_financeiro/
├── .streamlit/
│   └── secrets.toml      # Chaves de API para desenvolvimento local
├── app.py                # Ficheiro principal que executa a UI do Streamlit
├── app_ui.py             # Funções responsáveis por construir a UI
├── config.py             # Gestão de configuração e chaves de API
├── gemini_service.py     # Lógica de comunicação com a API do Gemini
├── olx_service.py        # Lógica para recolher dados da API do OLX
├── prompt.py             # Armazena e formata os prompts para a IA
├── utils.py              # Funções de utilidade (ex: ler ficheiros)
├── vercel.json           # Ficheiro de configuração para o deploy na Vercel
└── requirements.txt      # Lista de dependências Python do projeto
🚀 Como Executar Localmente
Siga estes passos para configurar e executar o projeto na sua máquina.

1. Pré-requisitos
Python 3.9 ou superior

Uma chave de API do Google AI Studio (Gemini)

2. Clonar o Repositório
Bash

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
3. Criar um Ambiente Virtual e Instalar Dependências
É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

Bash

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate

# Ativar o ambiente (macOS/Linux)
source venv/bin/activate

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
4. Configurar as Chaves de API (Secrets)
Para desenvolvimento local, o Streamlit utiliza um ficheiro secrets.toml.

Crie uma pasta .streamlit na raiz do projeto.

Dentro dela, crie um ficheiro chamado secrets.toml com o seguinte conteúdo:

Ini, TOML

# .streamlit/secrets.toml
GEMINI_API_KEY = "sua-chave-api-do-gemini-aqui"
5. Executar a Aplicação
Com o ambiente virtual ativado, execute o seguinte comando no terminal:

Bash

streamlit run app.py
A aplicação será aberta automaticamente no seu navegador. Para a funcionalidade de dados em tempo real, será necessário obter e colar o seu Bearer Token do OLX no campo apropriado na barra lateral.

☁️ Deploy na Vercel
Este projeto está pronto para ser implementado na Vercel.

Faça o push do seu código para um repositório no GitHub, GitLab ou Bitbucket.

Configure as Variáveis de Ambiente no painel do seu projeto na Vercel. Adicione a GEMINI_API_KEY. O código em config.py já está preparado para ler esta variável.

Importe o seu projeto na Vercel. A Vercel irá detetar automaticamente o ficheiro vercel.json e implementar a aplicação.

Nota: Para uma aplicação pública e estável, recomenda-se a "Opção A" descrita na nossa conversa: recolher os dados uma vez, guardá-los num ficheiro .json e modificar o app.py para ler esse ficheiro, em vez de depender de um Bearer Token manual.

```python
print("Modelos disponíveis:")
for m in genai.list_models():
  # Verifica se o modelo suporta o método 'generateContent'
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

```

models/gemini-2.5-pro-preview-03-25
models/gemini-2.5-flash-preview-05-20
models/gemini-2.5-flash
models/gemini-2.5-flash-lite-preview-06-17
models/gemini-2.5-pro-preview-05-06
models/gemini-2.5-pro-preview-06-05
models/gemini-2.5-pro
models/gemini-2.0-flash-exp
models/gemini-2.0-flash
models/gemini-2.0-flash-001
models/gemini-2.0-flash-lite-001
models/gemini-2.0-flash-lite
models/gemini-2.0-flash-lite-preview-02-05
models/gemini-2.0-flash-lite-preview
models/gemini-2.0-pro-exp
models/gemini-2.0-pro-exp-02-05
models/gemini-exp-1206
models/gemini-2.0-flash-thinking-exp-01-21
models/gemini-2.0-flash-thinking-exp
models/gemini-2.0-flash-thinking-exp-1219
models/gemini-2.5-flash-preview-tts
models/gemini-2.5-pro-preview-tts
models/learnlm-2.0-flash-experimental
models/gemma-3-1b-it
models/gemma-3-4b-it
models/gemma-3-12b-it
models/gemma-3-27b-it
models/gemma-3n-e4b-it
models/gemma-3n-e2b-it
models/gemini-flash-latest
models/gemini-flash-lite-latest
models/gemini-pro-latest
models/gemini-2.5-flash-lite
models/gemini-2.5-flash-image-preview
models/gemini-2.5-flash-preview-09-2025
models/gemini-2.5-flash-lite-preview-09-2025
models/gemini-robotics-er-1.5-preview

```bash 
pip install -r requirements.txt
```
```bash 
streamlit run app.py
```