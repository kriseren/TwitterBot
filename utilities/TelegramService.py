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


async def send_telegram_message(chat_id, message):
    """
    Función que envía un mensaje de Telegram a través del chat pasado como parámetro.
    :param chat_id: El identificador del chat de telegram a través del cual se enviará el mensaje.
    :param message: El mensaje a enviar en forma de cadena de caracteres.
    :return: No devuelve nada.
    """
    # Crea una instancia del bot de Telegram
    bot = Bot(token=tkn.telegram_token)

    # Envía el mensaje al chat especificado
    await bot.send_message(chat_id=chat_id, text=message)
    # Cierra la sesión del bot.
    session = await bot.get_session()
    await session.close()
