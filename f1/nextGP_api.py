import datetime
import requests
import json
from twilio.rest import Client

# Función que obtiene el siguiente Gran Premio a partir de una lista de Grandes Premios.
def get_next_gp(gps):

    today = datetime.date.today()
    gp_cercano = min(gps, key=lambda gp: datetime.datetime.strptime(gp["date"], '%Y-%m-%d').date() - today if datetime.datetime.strptime(gp["date"], '%Y-%m-%d').date() > today else datetime.timedelta(days=365*100))

    return gp_cercano

# Función que obtiene el número de días que quedan para el siguiente Gran Premio.
def get_days_left(gp):

    today = datetime.date.today()
    fecha_gp = datetime.datetime.strptime(gp['date'], '%Y-%m-%d').date()
    days_left = (fecha_gp - today).days

    return days_left

# Función que crea el tweet que se va a publicar en función del gran premio pasado como parámetro.
def create_tweet(gp):

    pais = gp['Circuit']['Location']['country']
    circuito = gp['Circuit']['circuitName']
    fecha_hora = gp['date'] + ' ' + gp['time']
    tweet = f"Quedan {get_days_left(gp)} días para el Gran Premio de {pais} en {circuito}. Fecha y hora: {fecha_hora} 🏎️🏁 #F1"

    return tweet

# Función que inicia sesión en Sinch, la API de Whatsapp y envía el mensaje pasado como parámetro.
def send_whatsapp_message(message):

    account_sid = 'AC936a26fe8433ac48ca3b854bfd3e543b'
    auth_token = '7e534e8ccad3dc47f67d7ecea724e633'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      from_='whatsapp:+14155238886',
      body=message,
      to='whatsapp:+34606152837'
    )

    print(message.sid)

# Función principal del programa que llama a los demás métodos.
def main():

    response = requests.get('https://ergast.com/api/f1/current.json')
    gps = response.json()['MRData']['RaceTable']['Races']
    gp_cercano = get_next_gp(gps)
    tweet = create_tweet(gp_cercano)
    send_whatsapp_message(tweet)

# Comprobación necesaria de Python para que se ejecute Main.
if __name__ == '__main__':
    main()
