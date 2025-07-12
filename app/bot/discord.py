import discord
import os
import dotenv
from llm import full_chain

# Carregar variáveis de ambiente do arquivo .env
dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Definir as intenções (intents) necessárias para o bot
# O bot precisa de permissão para ler o conteúdo das mensagens
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Inicializar o cliente do Discord
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    Evento que é acionado quando o bot se conecta com sucesso ao Discord.
    """
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    """
    Evento que é acionado a cada mensagem recebida.
    """
    # Ignorar mensagens do próprio bot para evitar loops infinitos
    if message.author == client.user:
        return

    # Verificar se o bot foi mencionado na mensagem
    if client.user.mentioned_in(message):
        print(f"Bot mencionado por: {message.author}")
        
        # Usar 'typing' para indicar que o bot está "pensando"
        async with message.channel.typing():
            # Remover a menção do bot da mensagem para obter a pergunta limpa
            question = message.content.replace(f'<@!{client.user.id}>', '').strip()
            print(f"Pergunta recebida: '{question}'")

            # Invocar a cadeia da LangChain para obter a resposta
            response = full_chain.invoke({"question": question})
            print(f"Resposta da chain: '{response}'")
            # Enviar a resposta de volta para o canal do Discord
            await message.channel.send(response)

def start():
    # Iniciar o bot com o token
    if DISCORD_TOKEN:
        client.run(DISCORD_TOKEN)
    else:
        print("Erro: O DISCORD_TOKEN não foi encontrado no arquivo .env")