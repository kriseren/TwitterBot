import datetime
import requests
import tweepy
import Main
from auth import tokens as tkn
import asyncio
from aiogram import Bot


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
    print(gp)
    pais = gp['Circuit']['Location']['country']
    ronda = gp['round']
    circuito = gp['Circuit']['circuitName']
    fecha_hora = gp['date'] + ' ' + gp['time']
    tweet = f"¿¡PREPARADXS PARA LA CARRERA Nº{ronda}!?\nQuedan {get_days_left(gp)} días para el Gran Premio de {pais} en {circuito}. Fecha y hora: {fecha_hora} 🏎️🏁"

    return tweet

# Función que envía un mensaje de Telegram a través del chat pasado como parámetro.
async def enviar_mensaje_telegram(chat_id, message):
    # Crea una instancia del bot de Telegram
    bot = Bot(token=tkn.telegram_token)

    # Envía el mensaje al chat especificado
    await bot.send_message(chat_id=chat_id, text=message)
    await bot.close_bot()

# Función principal del programa que llama a los demás métodos.
def main(client: tweepy.Client):
    Main.print_title_message(f"F1 REMINDER SCRIPT INITIALISED AT {Main.get_time()}")

    # Obtiene la información del próximo Gran Premio.
    response = requests.get('https://ergast.com/api/f1/current.json')
    gps = response.json()['MRData']['RaceTable']['Races']
    gp_cercano = get_next_gp(gps)

    # Crea el texto a enviar.
    message = create_message(gp_cercano)

    # Envía el mensaje por Telegram al grupo de F1 Fans.
    asyncio.run(enviar_mensaje_telegram(chat_id=tkn.telegram_f1_group_id, message=message))

    # Sube el tweet con el mensaje.
    Main.print_message("TWEET CONTENT", message)
    try:
        #client.create_tweet(text=message)
        Main.print_message("F1 REMINDER TWEET STATUS","F1 reminder tweet upload successful.","green")
    except Exception as ex:
        Main.print_message("F1 REMINDER TWEET STATUS", "F1 reminder tweet upload failed.", "red")
        Main.print_message("ERROR MESSAGE",str(ex),"red")

# Comprobación necesaria de Python para que se ejecute Main.
if __name__ == '__main__':
    main()
