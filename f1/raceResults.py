import asyncio
from datetime import datetime

import requests
from utilities.TelegramService import send_telegram_message

from auth import tokens as tkn, auth_utilities
from utilities import Translator
from utilities.Printer import print_message, print_title_message


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


def create_message_and_tweet(last_race_results):
    """
    Función que crea el texto del tweet con los resultados de la última carrera.
    """
    # Obtener información relevante de los resultados.
    race_name = last_race_results["raceName"]
    country = last_race_results["Circuit"]["Location"]["country"]

    # Crear el encabezado del tweet.
    tweet_text = Translator.translate(f"🏁 Results from the {race_name}:") + "\n\n"

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


def main(client):
    print_title_message(f"F1 RACE RESULT SCRIPT INITIALISED AT {datetime.now()}")

    # Obtener los resultados de la última carrera
    last_race_results = get_last_race_results()

    if last_race_results:
        # Crear el texto del tweet
        message_and_tweet = create_message_and_tweet(last_race_results)

        # Envía el mensaje por Telegram al grupo de F1 Fans.
        print_message("MESSAGE CONTENT", message_and_tweet)
        try:
            asyncio.run(send_telegram_message(chat_id=tkn.telegram_f1_group_id, message=message_and_tweet))
            print_message("F1 RACE RESULT MESSAGE STATUS", "F1 race result message_and_tweet sending successful.",
                          "green")
        except Exception as ex:
            print_message("F1 RACE RESULT MESSAGE STATUS", "F1 race result message_and_tweet sending failed.", "red")
            print_message("ERROR MESSAGE", str(ex), "red")

        # Sube el tweet con el mensaje.
        print_message("TWEET CONTENT", message_and_tweet)
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
