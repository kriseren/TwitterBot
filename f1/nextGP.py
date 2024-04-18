import asyncio
import datetime
import locale

import pytz
import requests
from aiogram import Bot

from auth import tokens as tkn, auth_utilities
from utilities.Printer import print_message, print_title_message


def get_next_gp(gps):
    """
    Obtiene el siguiente Gran Premio a partir de una lista de Grandes Premios.

    Args:
        gps (list): Lista de Grandes Premios.

    Returns:
        dict: Información del próximo Gran Premio.
    """
    today = datetime.date.today()
    next_gp = min(gps, key=lambda gp: datetime.datetime.strptime(gp["date"],
                                                                 '%Y-%m-%d').date() - today if datetime.datetime.strptime(
        gp["date"], '%Y-%m-%d').date() >= today else datetime.timedelta(days=365 * 100))
    return next_gp


def create_message_and_tweet(gp):
    """
    Crea el mensaje y el tweet para el Gran Premio dado.

    Args:
        gp (dict): Información del Gran Premio.

    Returns:
        list: Una lista que contiene el mensaje y el tweet.
    """
    country = gp['Circuit']['Location']['country']
    round_num = gp['round']
    circuit = gp['Circuit']['circuitName']
    date = gp['date']
    time = gp['time']
    days_left = (datetime.datetime.strptime(gp['date'], '%Y-%m-%d').date() - datetime.date.today()).days

    message = tweet = "Mensaje a enviar. Si lees esto es que ha dado error y no se ha asignado nunca."

    if days_left == 0:
        tweet = message = f"🏁 ¡HOY ES EL DÍA SEÑORAS Y SEÑORES! 🏁\n¿Conseguirá el nano su victoria Nº33? Todos a ver la carrera a las {format_spanish_timezone(time)}"

    elif days_left <= 3:
        if 'Sprint' in gp:
            message = tweet = f"¿¡PREPARADXS PARA LA CARRERA Nº{round_num}!?\n" \
                              f"¡Apenas quedan {days_left} días para volver a disfrutar! 👇🏼\n\n" \
                              f"🏃 Ent. libres 1: {get_day_of_the_week(gp['FirstPractice']['date'])} a las {format_spanish_timezone(gp['FirstPractice']['time'])}\n\n" \
                              f"⏱ Clasif. Sprint: {get_day_of_the_week(gp['SecondPractice']['date'])} a las {format_spanish_timezone(gp['SecondPractice']['time'])}\n\n" \
                              f"🏁 Carrera Sprint: {get_day_of_the_week(gp['Sprint']['date'])} a las {format_spanish_timezone(gp['Sprint']['time'])}\n\n" \
                              f"⏱ Clasificación: {get_day_of_the_week(gp['Qualifying']['date'])} a las {format_spanish_timezone(gp['Qualifying']['time'])}\n\n" \
                              f"🏁 Carrera: {get_day_of_the_week(date)} a las {format_spanish_timezone(time)}\n"
        else:
            message = tweet = f"¿¡PREPARADXS PARA LA CARRERA Nº{round_num}!?\n" \
                              f"¡Solo {days_left} días para disfrutarlo! 👇🏼\n\n" \
                              f"🏃 Ent. libres 1: {get_day_of_the_week(gp['FirstPractice']['date'])} a las {format_spanish_timezone(gp['FirstPractice']['time'])}\n\n" \
                              f"🏃 Ent. libres 2: {get_day_of_the_week(gp['SecondPractice']['date'])} a las {format_spanish_timezone(gp['SecondPractice']['time'])}\n\n" \
                              f"🏃 Ent. libres 3: {get_day_of_the_week(gp['ThirdPractice']['date'])} a las {format_spanish_timezone(gp['ThirdPractice']['time'])}\n\n" \
                              f"⏱ Clasificación: {get_day_of_the_week(gp['Qualifying']['date'])} a las {format_spanish_timezone(gp['Qualifying']['time'])}\n\n" \
                              f"🏁 Carrera: {get_day_of_the_week(date)} a las {format_spanish_timezone(time)}\n"

    elif days_left < 7:
        tweet = message = f"¿¡PREPARADXS PARA LA CARRERA Nº{round_num}!?\nEntramos en semana de carrera y quedan {days_left} días para el Gran Premio de {country} en {circuit} este {date} a las {format_spanish_timezone(time)} 🏎️🏁"

    else:
        tweet = message = f"¿¡PREPARADXS PARA LA CARRERA Nº{round_num}!?\nQuedan {days_left} días para el Gran Premio de {country} en {circuit}. Fecha: {date}. Hora: {format_spanish_timezone(time)} 🏎️🏁"

    return [message, tweet]



async def send_telegram_message(chat_id, message):
    """
    Envía un mensaje de Telegram al chat especificado.

    Args:
        chat_id (str): El ID del chat de Telegram.
        message (str): El mensaje a enviar.
    """
    bot = Bot(token=tkn.telegram_token)
    await bot.send_message(chat_id=chat_id, text=message)
    session = await bot.get_session()
    await session.close()


def format_spanish_timezone(time_str: str):
    """
    Convierte una hora en formato UTC (Z) a la hora en la zona horaria de Madrid.

    Args:
        time_str (str): La hora en formato UTC (por ejemplo: "09:00:00Z").

    Returns:
        str: La hora convertida en la zona horaria de Madrid (por ejemplo: "11:00:00").
    """
    time_utc = datetime.datetime.strptime(time_str[:-1], "%H:%M:%S").time()
    timezone_madrid = pytz.timezone('Europe/Madrid')
    local_time_utc = datetime.datetime.utcnow().date()
    temp_datetime_utc = datetime.datetime.combine(local_time_utc, time_utc)
    hora_fecha_madrid = temp_datetime_utc.replace(tzinfo=pytz.utc).astimezone(timezone_madrid)
    formatted_time = hora_fecha_madrid.strftime("%H:%M")
    return formatted_time


def get_day_of_the_week(date: str):
    """
    Devuelve el nombre del día de la semana para una fecha dada.

    Args:
        date (str): La fecha en formato YYYY-MM-DD.

    Returns:
        str: El nombre del día de la semana (por ejemplo: "Domingo").
    """
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    except locale.Error:
        pass
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')
    nombre_dia = fecha.strftime('%A').capitalize()
    return nombre_dia


def main(client):
    """
    Función principal del script de recordatorio de F1.
    """
    print_title_message(f"F1 REMINDER SCRIPT INITIALISED AT {datetime.datetime.now()}")

    response = requests.get('https://ergast.com/api/f1/current.json')
    gps = response.json()['MRData']['RaceTable']['Races']
    gp_cercano = get_next_gp(gps)

    message_and_tweet = create_message_and_tweet(gp_cercano)

    print_message("MESSAGE CONTENT", message_and_tweet[0])
    try:
        asyncio.run(send_telegram_message(chat_id=tkn.telegram_f1_group_id, message=message_and_tweet[0]))
        print_message("F1 REMINDER MESSAGE STATUS", "F1 reminder message sending successful.", "green")
    except Exception as ex:
        print_message("F1 REMINDER MESSAGE STATUS", "F1 reminder message sending failed.", "red")
        print_message("ERROR MESSAGE", str(ex), "red")

    print_message("TWEET CONTENT", message_and_tweet[1])
    try:
        client.create_tweet(text=message_and_tweet[1])
        print_message("F1 REMINDER TWEET STATUS", "F1 reminder tweet upload successful.", "green")
    except Exception as ex:
        print_message("F1 REMINDER TWEET STATUS", "F1 reminder tweet upload failed.", "red")
        print_message("ERROR MESSAGE", str(ex), "red")


if __name__ == '__main__':
    # Autentica al cliente de Twitter.
    client = auth_utilities.authenticate_to_twitter()
    main(client)
