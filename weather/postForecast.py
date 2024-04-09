import tweepy
from auth import auth_utilities
from weather import weatherForecastExtract
from utilities.Printer import print_message, print_title_message
from datetime import datetime


def main(client):
    """
    Función principal para publicar la previsión meteorológica en Twitter.

    Args:
        client: Cliente de Twitter autenticado.
    """

    print_title_message(f"WEATHER FORECAST SCRIPT INITIALISED AT {datetime.now()}")

    # Obtención de datos meteorológicos.
    weather_data = weatherForecastExtract.getWeatherData("petrer")
    min_temp = weather_data["main"]["temp_min"]
    max_temp = weather_data["main"]["temp_max"]
    humidity = weather_data["main"]["humidity"]
    feels_like = weather_data["main"]["feels_like"]

    # Creación del contenido del tweet con los datos obtenidos.
    tweet_content = f"☁ PREVISIÓN METEOROLÓGICA ☁\n" \
                    f"¡Buenos días! Para hoy se esperan los siguientes datos:\n" \
                    f"Temperatura mínima: {min_temp}°C \t Temperatura máxima: {max_temp}°C\n" \
                    f"Sensación térmica: {feels_like}°C \t Humedad: {humidity}%\n" \
                    f"#weather #weatherforecast"

    # Subir el tweet
    print_message("WEATHER FORECAST", tweet_content)

    client.create_tweet(text=tweet_content)
    print_message("WEATHER FORECAST", "Tweet upload successful.")


if __name__ == '__main__':
    # Autenticación del cliente de Twitter.
    client = auth_utilities.authenticate_to_twitter()
    main(client)
