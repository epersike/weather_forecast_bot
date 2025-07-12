import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from .get_weather import get_weather_forecast

dotenv.load_dotenv()

# Use an OpenAI model. Make sure your .env file has the OPENAI_API_KEY.
chat_model = ChatOpenAI(model="gpt-4o", temperature=0)
output_parser = StrOutputParser()

# --- 1. CADEIA DE VALIDAÇÃO ---
# Esta cadeia verifica se a pergunta é sobre previsão do tempo.
# Responde com "VALIDO" ou "INVALIDO" para ser fácil de processar.
validation_template = """Sua tarefa é verificar se a pergunta do usuário é sobre previsão do tempo e se contém uma cidade.
A pergunta deve conter o nome da cidade e o país desejado. Se o usuário não informar o país, tente identificar qual o país baseado na cidade informada.
Se for uma pergunta válida sobre o tempo responda a cidade e país para qual o usuário solicitou a previsão 
separando a cidade e o país por vírgula. retorne o país com apenas dois caracteres no formato ISO 3166-1 alpha-2.
Se não for uma pergunta sobre o tempo, informando de qual cidade deseja obter a previsão responda apenas com a palavra 'INVALIDO'.

Pergunta do usuário:
{question}
"""
validation_prompt = ChatPromptTemplate.from_template(validation_template)
validation_chain = validation_prompt | chat_model | output_parser

# --- 2. CADEIA PRINCIPAL (PREVISÃO DO TEMPO) ---
# Esta cadeia é executada apenas se a validação for bem-sucedida.
weather_template_str = """Seu trabalho é usar os dados de previsão do tempo para
    responder a perguntas sobre a previsão para os próximos dias em uma determinada cidade.
    O usuário fará a pergunta em português. Responda em português.
    Responda à pergunta da forma mais curta possível, incluindo: Dia, Temperatura Mínima, Temperatura Máxima,
    soma de precipitação, direção do vento em pontos cardeais e velocidade do vento.

    Se o usuário pedir mais informações, use o contexto que você tem abaixo.
    Se a informação solicitada não existir, simplesmente responda
    com a resposta padrão e diga que você não tem a informação solicitada.
    
    Weather forecast data:
    
    {formatted_weather_data}
"""
weather_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", weather_template_str),
        ("human", "{question}"),
    ]
)
weather_chain = weather_prompt | chat_model | output_parser

# --- 3. CADEIA DE RESPOSTA INVÁLIDA ---
# Esta cadeia é executada se a validação falhar.
invalid_template = """Você é um assistente e sua função é responder que só pode fornecer informações sobre a previsão do tempo.
Responda em português.

Pergunta do usuário:
{question}
"""
invalid_prompt = ChatPromptTemplate.from_template(invalid_template)
invalid_chain = invalid_prompt | chat_model | output_parser

# --- 4. ORQUESTRAÇÃO ---

def route(data):
    """
    Função roteadora. Com base no resultado da validação ('location'),
    decide qual cadeia executar em seguida.
    """
    if "INVALIDO" in data["location"]:
        return invalid_chain
    
    # Se a localização for válida, cria uma nova cadeia que:
    # 1. Busca os dados do tempo usando a localização.
    # 2. Verifica se os dados foram encontrados.
    # 3. Executa a cadeia de resposta do tempo ou uma mensagem de erro.
    try:
        city, country_code = data["location"].split(", ")
    except ValueError:
        return lambda x: "Ocorreu um erro: o formato da localização retornado pelo assistente é inválido."

    fetch_and_run_chain = RunnablePassthrough.assign(
        formatted_weather_data=lambda x: get_weather_forecast(city, country_code)
    ) | RunnableBranch(
        # Se get_weather_forecast retornou None (cidade não encontrada), retorna uma mensagem de erro.
        (lambda x: x["formatted_weather_data"] is None, 
         lambda x: f"Desculpe, não consegui encontrar a previsão do tempo para {data['location']}."),
        # Caso contrário, executa a cadeia principal com os dados obtidos.
        weather_chain
    )
    return fetch_and_run_chain

# A cadeia completa primeiro obtém a localização e, em seguida, usa o roteador para decidir o próximo passo.
full_chain = RunnablePassthrough.assign(
    location=validation_chain
) | RunnableLambda(route)

def test():
    # --- TESTES ---

    question = "Qual a previsão do tempo para os próximos dias em blumenau?"
    print(question)
    response = full_chain.invoke({"question": question})
    print(response)

    # print("--- Teste com pergunta válida ---")
    # question_valida = "Qual a previsão completa para os próximos dois dias em Blumenau, Brasil?"
    # response = full_chain.invoke({"question": question_valida})
    # print(response)

    # print("--- Teste com pergunta específica válida ---")
    # question_valida = "Vai chover nos próximos dias em Blumenau, Brasil?"
    # response = full_chain.invoke({"question": question_valida})
    # print(response)

    # print("\n--- Teste com pergunta inválida ---")
    # question_invalida = "Qual a capital da Austrália?"
    # response = full_chain.invoke({"question": question_invalida})
    # print(response)

    # print("\n--- Teste com cidade inexistente ---")
    # question_inexistente = "Qual a previsão do tempo para Nárnia, BR?"
    # response = full_chain.invoke({"question": question_inexistente})
    # print(response)
