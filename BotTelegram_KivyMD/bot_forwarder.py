# bot_forwarder.py
import logging
from telethon import TelegramClient, events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ForwardBot:
    def __init__(self, api_id, api_hash, canal_origem, canais_destino):
        self.api_id = api_id
        self.api_hash = api_hash
        self.canal_origem = canal_origem
        self.canais_destino = canais_destino
        self.client = TelegramClient("userbot_session", api_id, api_hash)

    async def iniciar(self):
        """Inicia o bot e registra o evento de monitoramento"""
        await self.client.start()
        logger.info("Bot conectado ao Telegram ✅")
        logger.info(f"Monitorando canal de origem: {self.canal_origem}")
        logger.info(f"Canais de destino: {self.canais_destino}")

        # Escuta novas mensagens no canal de origem
        @self.client.on(events.NewMessage(chats=self.canal_origem))
        async def handler(event):
            mensagem = event.message.text or event.message.caption
            if not mensagem:
                return

            logger.info(f"Mensagem recebida: {mensagem}")

            # Encaminha para todos os canais de destino
            for canal_destino in self.canais_destino:
                try:
                    await self.client.send_message(canal_destino, mensagem)
                    logger.info(f"➡ Mensagem enviada para {canal_destino}")
                except Exception as e:
                    logger.error(f"Erro ao enviar para {canal_destino}: {e}")

        await self.client.run_until_disconnected()
