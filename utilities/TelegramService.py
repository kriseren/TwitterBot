from aiogram import Bot
from auth import tokens as tkn

async def send_error_message(message):
    """
    Envía un mensaje de error a través de Telegram.

    Args:
        message (str): Contenido del mensaje de error.
    """
    message_header = "🚨 KRISEREN BOT HA SUFRIDO UN ERROR 🚨️\n"
    message = f"{message_header}Lamentablemente, el bot de twitter ha sufrido un error. " \
              f"Deberías arreglarlo, así que te dejo aquí el mensaje del error:\n{message}"
    bot = Bot(token=tkn.telegram_token)
    await bot.send_message(chat_id=tkn.telegram_admin_chat_id, text=message)
    await bot.session.close()
