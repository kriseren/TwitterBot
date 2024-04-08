import asyncio
import datetime
import locale
import pytz
import requests
import tweepy
from aiogram import Bot
from termcolor import termcolor
from googletrans import Translator
import Main
from auth import tokens as tkn, auth_utilities


def get_last_race_results():
    """
    Función que obtiene los resultados de la última carrera de Fórmula 1.
    """
    # URL del endpoint de resultados de la última carrera.
    url = "http://ergast.com/api/f1/current/last/results.json"

    # Realizar la solicitud GET al endpoint.
    response = requests.get(url)

    # Comprobar si la solicitud fue exitosa.
    if response.status_code == 200:
        # Convertir la respuesta a formato JSON.
        data = response.json()

        # Obtener los resultados de la última carrera.
        last_race_results = data["MRData"]["RaceTable"]["Races"][0]

        return last_race_results
    else:
        print("Error al obtener los resultados de la última carrera:", response.status_code)
        return None


def translate(text):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='es')
        return translated_text.text
    except Exception as e:
        print("Error occurred:", e)
        return None


def create_message_and_tweet(last_race_results):
    """
    Función que crea el texto del tweet con los resultados de la última carrera.
    """
    # Obtener información relevante de los resultados.
    race_name = last_race_results["raceName"]
    country = last_race_results["Circuit"]["Location"]["country"]

    # Crear el encabezado del tweet.
    tweet_text = translate(f"🏁 Results from the {race_name}:") + "\n\n"

    # Agregar los resultados de cada piloto al tweet.
    for i, result in enumerate(last_race_results["Results"][:10], 1):
        driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"

        # Determinar el emoji de medalla para las primeras tres posiciones
        medal_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else " "

        # Si el número es 10, asegurarse de que ambos dígitos tengan el emoticono
        if i == 10:
            tweet_text += "🔟"
        else:
            tweet_text += f"{i}️⃣"

        # Agregar el nombre del piloto y el emoji de la medalla al tweet
        tweet_text += f" {driver} {medal_emoji}\n"

    # Agregar hashtags y detalles adicionales al tweet.
    tweet_text += f"\n#F1 #{country}GP 🏎️🔥"

    return tweet_text


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


# Método que imprime por pantalla un mensaje pasado como parámetro.
def print_message(title: str, content: str, color: str = "white"):
    if color != "white":
        # Imprime el mensaje.
        print(termcolor.colored(f"[{title}]: {content}", color))
    else:
        # Imprime el mensaje.
        print(f"[{title}]: {content}")


# Método que imprime por pantalla un mensaje pasado como parámetro.
def print_title_message(content):
    # Calcula la longitud del mensaje y de la ventana.
    message_length = len(content)
    window_width = 80

    # Calcula los separadores.
    separator_length = (window_width - message_length) // 2
    left_separator = "-" * separator_length
    right_separator = "-" * (window_width - message_length - separator_length)

    # Imprime el mensaje.
    print(f"\n{left_separator} {content} {right_separator}")


def main(client):
    print_title_message(f"F1 RACE RESULT SCRIPT INITIALISED AT {Main.get_time()}")

    # Obtener los resultados de la última carrera
    last_race_results = get_last_race_results()

    if last_race_results:
        # Crear el texto del tweet
        message_and_tweet = create_message_and_tweet(last_race_results)

        # Envía el mensaje por Telegram al grupo de F1 Fans.
        Main.print_message("MESSAGE CONTENT", message_and_tweet)
        try:
            asyncio.run(send_telegram_message(chat_id=tkn.telegram_f1_group_id, message=message_and_tweet))
            print_message("F1 RACE RESULT MESSAGE STATUS", "F1 race result message_and_tweet sending successful.",
                          "green")
        except Exception as ex:
            print_message("F1 RACE RESULT MESSAGE STATUS", "F1 race result message_and_tweet sending failed.", "red")
            print_message("ERROR MESSAGE", str(ex), "red")

        # Sube el tweet con el mensaje.
        Main.print_message("TWEET CONTENT", message_and_tweet)
        try:
            client.create_tweet(text=message_and_tweet)
            print_message("F1 REMINDER TWEET STATUS", "F1 race result tweet upload successful.", "green")
        except Exception as ex:
            print_message("F1 REMINDER TWEET STATUS", "F1 race result tweet upload failed.", "red")
            print_message("ERROR MESSAGE", str(ex), "red")


if __name__ == "__main__":
    # Crea un cliente de Twitter
    client = auth_utilities.authenticate_to_twitter()

    # Llama a la función main con el cliente de Twitter como argumento
    main(client)
