import asyncio
import datetime
import locale
import pytz
import requests
import tweepy
from aiogram import Bot
import Main
from auth import tokens as tkn


# Función que obtiene el siguiente Gran Premio a partir de una lista de Grandes Premios.
def get_next_gp(gps):
    today = datetime.date.today()
    gp_cercano = min(gps, key=lambda gp: datetime.datetime.strptime(gp["date"],
                                                                    '%Y-%m-%d').date() - today if datetime.datetime.strptime(
        gp["date"], '%Y-%m-%d').date() >= today else datetime.timedelta(days=365 * 100))

    return gp_cercano


# Función que obtiene el número de días que quedan para el siguiente Gran Premio.
def get_days_left(gp):
    today = datetime.date.today()
    fecha_gp = datetime.datetime.strptime(gp['date'], '%Y-%m-%d').date()
    days_left = (fecha_gp - today).days

    return days_left


# Función que devuelve el nombre del día de una fecha pasada como parámetro.
def get_day_of_the_week(date):
    # Establece la configuración regional en español.
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    except locale.Error:
        # Si no se encuentra la configuración regional en español, se usa la configuración regional predeterminada
        pass

    # Convierte la fecha pasada como parámetro en un objeto date.
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')

    # Obtiene el nombre del día de la semana en español.
    nombre_dia = fecha.strftime('%A').capitalize()

    return nombre_dia


# Función que convierte una hora en formato UTC (Z) a la hora en la zona horaria de Madrid.
def format_spanish_timezone(time_str):
    # Convierte la hora UTC pasada como parámetro en un objeto Time.
    time_utc = datetime.datetime.strptime(time_str[:-1], "%H:%M:%S").time()

    # Crea un objeto de zona horaria para Madrid.
    timezone_madrid = pytz.timezone('Europe/Madrid')

    # Crea un objeto de fecha actual en UTC.
    local_time_utc = datetime.datetime.utcnow().date()

    # Combina la fecha actual en UTC con la hora especificada.
    temp_datetime_utc = datetime.datetime.combine(local_time_utc, time_utc)

    # Convierte la hora especificada de UTC a la zona horaria de Madrid.
    hora_fecha_madrid = temp_datetime_utc.replace(tzinfo=pytz.utc).astimezone(timezone_madrid)

    # Extrae la hora convertida en Madrid
    formatted_time = hora_fecha_madrid.strftime("%H:%M")

    return formatted_time


# Función que crea el tweet que se va a publicar en función del gran premio pasado como parámetro.
def create_message_and_tweet(gp):
    # Se extraen todos los datos en variables locales.
    country = gp['Circuit']['Location']['country']
    round = gp['round']
    circuit = gp['Circuit']['circuitName']
    date = gp['date']
    time = gp['time']
    days_left = get_days_left(gp)
    message = "Mensaje a enviar. Si lees esto es que ha dado error y no se ha asignado nunca."
    tweet = "Mensaje a enviar. Si lees esto es que ha dado error y no se ha asignado nunca."

    # Si es el mismo día de la carrera.
    if days_left == 0:
        # Se asigna el mismo valor a las dos variables.
        tweet = message = f"🏁 ¡HOY ES EL DÍA SEÑORAS Y SEÑORES! 🏁\n¿Conseguirá el nano su victoria Nº33?"

    # Si queda menos de una semana, se muestran los horarios detallados.
    elif days_left <= 7:
        # Crea la parte común para todas las careras.
        message = f"¿¡PREPARADXS PARA LA CARRERA Nº{round}!?\n" \
                  f"Estamos en semana de Gran Premio y apenas quedan {days_left} días, así que nunca está de más recordar los horarios 👇🏼\n\n" \
                  f"🏃 Entrenamientos libres 1: {get_day_of_the_week(gp['FirstPractice']['date'])} a las {format_spanish_timezone(gp['FirstPractice']['time'])}\n\n" \
                  f"🏃 Entrenamientos libres 2: {get_day_of_the_week(gp['SecondPractice']['date'])} a las {format_spanish_timezone(gp['SecondPractice']['time'])}\n\n" \
 \
        # Si hay Entrenamientos libres 3 significa que no es Sprint.
        # TODO buscar una manera de saber si hay sprint o carrera normal y que sea dinámico.

        # Se completa el mensaje.
        message = message + f"⏱  Clasificación: {get_day_of_the_week(gp['Qualifying']['date'])} a las {format_spanish_timezone(gp['Qualifying']['time'])}\n\n" \
                            f"🏁 Carrera: {get_day_of_the_week(date)} a las {format_spanish_timezone(time)}\n"

    # Si queda más de una semana.
    else:
        tweet = message = f"¿¡PREPARADXS PARA LA CARRERA Nº{round}!?\nQuedan {days_left} días para el Gran Premio de {country} en {circuit}. Fecha: {date}. Hora: {format_spanish_timezone(time)} 🏎️🏁"

    return [message, tweet]

# Función que envía un mensaje de Telegram a través del chat pasado como parámetro.
async def send_telegram_message(chat_id, message):
    # Crea una instancia del bot de Telegram
    bot = Bot(token=tkn.telegram_token)

    # Envía el mensaje al chat especificado
    await bot.send_message(chat_id=chat_id, text=message)
    # Cierra la sesión del bot.
    session = await bot.get_session()
    await session.close()


def main(client: tweepy.Client):
    Main.print_title_message(f"F1 REMINDER SCRIPT INITIALISED AT {Main.get_time()}")

    # Obtiene la información del próximo Gran Premio.
    response = requests.get('https://ergast.com/api/f1/current.json')
    gps = response.json()['MRData']['RaceTable']['Races']
    gp_cercano = get_next_gp(gps)

    # Crea el texto a enviar y a subir.
    message_and_tweet = create_message_and_tweet(gp_cercano)

    # Envía el mensaje por Telegram al grupo de F1 Fans.
    Main.print_message("MESSAGE CONTENT", message_and_tweet[0])
    try:
        asyncio.run(send_telegram_message(chat_id=tkn.telegram_f1_group_id, message=message_and_tweet[0]))
        Main.print_message("F1 REMINDER MESSAGE STATUS", "F1 reminder message_and_tweet sending successful.", "green")
    except Exception as ex:
        Main.print_message("F1 REMINDER MESSAGE STATUS", "F1 reminder message_and_tweet sending failed.", "red")
        Main.print_message("ERROR MESSAGE", str(ex), "red")

    # Sube el tweet con el mensaje.
    Main.print_message("TWEET CONTENT", message_and_tweet[1])
    try:
        client.create_tweet(text=message_and_tweet[1])
        Main.print_message("F1 REMINDER TWEET STATUS", "F1 reminder tweet upload successful.", "green")
    except Exception as ex:
        Main.print_message("F1 REMINDER TWEET STATUS", "F1 reminder tweet upload failed.", "red")
        Main.print_message("ERROR MESSAGE", str(ex), "red")
