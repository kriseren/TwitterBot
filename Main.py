import datetime
import time

from auth import auth_utilities
from f1 import nextGP
from music import postRecommendation


# Método que obtiene la hora y la fecha actuales.
def get_time():
    return datetime.datetime.now()


# Método que imprime por pantalla un mensaje pasado como parámetro.
def print_message(message):
    # Calcula la longitud del mensaje y de la ventana.
    message_length = len(message)
    window_width = 80

    # Calcula los separadores.
    separator_length = (window_width - message_length) // 2
    left_separator = "-" * separator_length
    right_separator = "-" * (window_width - message_length - separator_length)

    # Imprime el mensaje.
    print(f"\n{left_separator} {message} {right_separator}")


# Método principal del programa.
def main():
    print_message(f"BOT INITIALISED AT {get_time()}")

    # Inicia sesión en la API de Twitter.
    client = auth_utilities.authenticate_to_twitter()

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

        # Verifica si ha entrado algún tweet nuevo.
        # mentions.check_new_mention()

        # Pausar el programa durante un minuto antes de verificar la hora nuevamente.
        time.sleep(60)


if __name__ == '__main__':
    main()
