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


async def send_telegram_message(chat_id, message, photo_path=None):
    """
    Función que envía un mensaje de Telegram a través del chat pasado como parámetro, junto con una imagen adjunta opcional.
    :param chat_id: El identificador del chat de telegram a través del cual se enviará el mensaje.
    :param message: El mensaje a enviar en forma de cadena de caracteres.
    :param photo_path: La ruta de la imagen que se adjuntará al mensaje (opcional).
    :return: No devuelve nada.
    """
    # Crea una instancia del bot de Telegram
    bot = Bot(token=tkn.telegram_token)

    # Envía el mensaje de texto
    await bot.send_message(chat_id=chat_id, text=message)

    # Si se proporcionó una ruta de imagen, envía la imagen adjunta
    if photo_path:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo)

    await bot.session.close()