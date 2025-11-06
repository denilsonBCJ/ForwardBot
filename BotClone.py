from telethon import TelegramClient, events
import logging

# Configuração da API do Telegram
API_ID = 26032023  # Substitua pelo seu API ID
API_HASH = "206f2f60dfa36052d1c3db6775cfc76e"  # Substitua pelo seu API Hash
CANAL_ORIGEM = -1002352946067  # ID do canal de origem (onde as mensagens serão lidas)
CANAL_DESTINO = -1002693629264  # ID do canal de destino (onde as mensagens serão enviadas)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criando o cliente Telethon (Userbot)
client = TelegramClient("userbot_session", API_ID, API_HASH)

# Evento que monitora novas mensagens no canal de origem
@client.on(events.NewMessage(chats=CANAL_ORIGEM))
async def forward_message(event):
    mensagem = event.message.text or event.message.caption  # Pega o texto da mensagem
    if mensagem:
        logger.info(f"Mensagem recebida: {mensagem}")
        # Envia a mensagem para o canal de destino
        try:
            await client.send_message(CANAL_DESTINO, mensagem)
            logger.info("Mensagem encaminhada com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao encaminhar mensagem: {e}")
    else:
        logger.info("Mensagem sem texto para encaminhar")

# Função principal assíncrona
async def main():
    print("Userbot rodando...")

    # Faz login (primeira vez pode pedir código de verificação via SMS ou Telegram)
    await client.start()

    # Inicia o loop para monitorar novas mensagens e responder
    await client.run_until_disconnected()

# Executa a função principal
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Usa asyncio para rodar a função main assíncrona
