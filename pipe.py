from langchain_ollama import ChatOllama
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from langchain_core.output_parsers import StrOutputParser
from get_weather import get_weather_forecast
from utils import reformat_weather_data


# 1 - Load forecast info:
weather_data = get_weather_forecast()
formatted_weather_data = reformat_weather_data(weather_data)

# 1 - Verificar se o usuário está pedindo por uma previsão do tempo....
validate_template_str = """
    Verifique se o usuário está pedindo por uma previsão do tempo.
    Verifique se o usuário forneceu a informação do local que deseja a previsão, 
    informando o nome da cidade/localidade e o código do país no formato ISO 3166-1 alpha-2.
    Caso o usuário não tenha informado, responda dizendo que ele deve informar a cidade
    e o código do país, listando para o usuário todos os códigos válidos de países do formato ISO 3166-1 alpha-2.
"""

validate_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[],
        template=validate_template_str,
    )
)



# 3 - Create weather forecast template
weather_template_str = """Seu trabalho é usar os dados de previsão do tempo para
    responder a perguntas sobre a previsão para os próximos dias em uma determinada cidade.
    O usuário fará a pergunta em português. Responda em português.
    Responda à pergunta da forma mais curta possível. A
    default answer should be: Day, Min temperature, Max temperature,
    precipitation sum, wind direction and wind speed.
    Se o usuário pedir mais informações, use o contexto que você tem abaixo.
    Se a informação solicitada não existir, simplesmente responda
    com a resposta padrão e diga que você não tem a informação solicitada.
    By default, you only have information about the next 7 days, if asked
    about other dates, simple state your limitation.
    
    Weather forecast data:
    
    {formatted_weather_data}
"""

weather_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["formatted_weather_data"],
        template=weather_template_str,
    )
)

weather_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)
messages = [validate_system_prompt, weather_system_prompt, weather_human_prompt]

weather_prompt_template = ChatPromptTemplate(
    input_variables=["formatted_weather_data", "question"],
    messages=messages,
)

# Use a local model with Ollama. Make sure Ollama is running with the specified model.
# You can use other models like 'mistral', 'llama2', etc.
chat_model = ChatOllama(model="llama3", temperature=0)

output_parser = StrOutputParser()

review_chain = weather_prompt_template | chat_model | output_parser

# question = "Amanhã, dia 2025-07-12, vai chover?"
question = "What's the full weather forecast for the next two days?"
response = review_chain.invoke({"formatted_weather_data": formatted_weather_data, "question": question})
print(response)
