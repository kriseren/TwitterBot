import telegram
import auth.tokens as tkn

import asyncio
from aiogram import Bot

async def enviar_mensaje_telegram(chat_id, mensaje):
    # Crea una instancia del bot de Telegram
    bot = Bot(token=tkn.telegram_token)

    # Envía el mensaje al chat especificado
    await bot.send_message(chat_id=chat_id, text=mensaje)

# Llamada a la función asincrónica y espera a que se complete
asyncio.run(enviar_mensaje_telegram(chat_id=tkn.telegram_f1_group_id, mensaje='Test4'))

