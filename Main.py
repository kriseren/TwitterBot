import datetime
import time

import termcolor
from twilio.rest import Client
from auth import auth_utilities
from auth import tokens as tkn
from f1 import nextGP
from music import postRecommendation
from common_actions import mentions


# Método que obtiene la hora y la fecha actuales.
def get_time():
    return datetime.datetime.now()

# Método que imprime por pantalla un mensaje pasado como parámetro.
def print_message(title: str,content: str,color: str = "white"):
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

# Función que inicia sesión en Twilio, la API de Whatsapp y envía el mensaje pasado como parámetro.
def send_error_message(message: str, receiver_number: str):
    twilio_client = Client(tkn.twilio_sid, tkn.twilio_token)

    twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:+34{receiver_number}'
    )

# Método principal del programa.
def main():
    print_title_message(f"BOT INITIALISED AT {get_time()}")

    # Inicia sesión en la API de Twitter.
    client = auth_utilities.authenticate_to_twitter()

    try:
        # Bucle principal del programa dentro del cual se comprueba la hora.
        while True:

            # Obtiene la fecha y la hora actuales.
            now = get_time()

            # Verifica si es la hora programada para subir la recomendación musical del día.
            if now.hour == 14 and now.minute == 00:
                postRecommendation.main(client)

            # Verifica si es la hora programada para subir el tweet sobre la F1 del día.
            elif now.hour == 18 and now.minute == 30:
                nextGP.main(client)
            else:
                pass

            # Verifica si ha entrado algún tweet nuevo y lo gestiona.
            mentions.main(client)

            # Pausar el programa durante un minuto antes de verificar la hora nuevamente.
            time.sleep(60)
    except Exception as ex:
        send_error_message(f"ERROR {str(ex)}",tkn.admin_telephone)


if __name__ == '__main__':
    main()
