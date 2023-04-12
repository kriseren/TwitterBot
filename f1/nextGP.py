import datetime

import requests
import tweepy
from termcolor import colored
from twilio.rest import Client

import Main
from auth import tokens as tkn


# Función que obtiene el siguiente Gran Premio a partir de una lista de Grandes Premios.
def get_next_gp(gps):
    today = datetime.date.today()
    gp_cercano = min(gps, key=lambda gp: datetime.datetime.strptime(gp["date"],
                                                                    '%Y-%m-%d').date() - today if datetime.datetime.strptime(
        gp["date"], '%Y-%m-%d').date() > today else datetime.timedelta(days=365 * 100))

    return gp_cercano


# Función que obtiene el número de días que quedan para el siguiente Gran Premio.
def get_days_left(gp):
    today = datetime.date.today()
    fecha_gp = datetime.datetime.strptime(gp['date'], '%Y-%m-%d').date()
    days_left = (fecha_gp - today).days

    return days_left


# Función que crea el tweet que se va a publicar en función del gran premio pasado como parámetro.
def create_message(gp):
    pais = gp['Circuit']['Location']['country']
    circuito = gp['Circuit']['circuitName']
    fecha_hora = gp['date'] + ' ' + gp['time']
    tweet = f"Quedan {get_days_left(gp)} días para el Gran Premio de {pais} en {circuito}. Fecha y hora: {fecha_hora} 🏎️🏁 #F1"

    return tweet


# Función que inicia sesión en Twilio, la API de Whatsapp y envía el mensaje pasado como parámetro.
def send_whatsapp_message(message: str, receiver_number: str):
    twilio_client = Client(tkn.twilio_sid, tkn.twilio_token)

    twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:+34{receiver_number}'
    )


# Método que lee el fichero de lista de números de teléfono y los carga a un array.
def load_telephone_numbers():
    with open('f1/lista_difusion.txt', 'r') as f:
        return f.readlines()


# Función principal del programa que llama a los demás métodos.
def main(client: tweepy.Client):
    Main.print_message(f"F1 REMINDER SCRIPT INITIALISED AT {Main.get_time()}")

    # Obtiene la información del próximo Gran Premio.
    response = requests.get('https://ergast.com/api/f1/current.json')
    gps = response.json()['MRData']['RaceTable']['Races']
    gp_cercano = get_next_gp(gps)

    # Crea el texto a enviar.
    message = create_message(gp_cercano)

    # Por cada número en la lista de difusión envía un Whatsapp.
    for number in load_telephone_numbers():
        send_whatsapp_message(message, number)

    # Sube el tweet con el mensaje.
    print("\n[TWEET CONTENT]\n", message)
    try:
        client.create_tweet(text=message)
        print(colored("\n[TWEET STATUS]: F1 reminder upload successful.", "green"))
    except Exception as ex:
        print(colored("\n[TWEET STATUS]: F1 reminder upload failed", "red"))
        print(colored(f"\n[ERROR MESSAGE]: {str(ex)}", "red"))


# Comprobación necesaria de Python para que se ejecute Main.
if __name__ == '__main__':
    main()
