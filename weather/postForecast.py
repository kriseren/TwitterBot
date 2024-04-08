from auth import auth_utilities
from weather import weatherForecastExtract

def main():
    # Autenticación en twitter.
    client = auth_utilities.authenticate_to_twitter()

    # Obtención de datos meteorológicos.
    weatherData = weatherForecastExtract.getWeatherData("petrer")
    min = weatherData["main"]["temp_min"]
    max = weatherData["main"]["temp_max"]
    media = min + max / 2
    humidity = weatherData["main"]["humidity"]
    temp = weatherData["main"]["temp"]
    sensacion = weatherData["main"]["feels_like"]

    # Creación del tweet con los datos obtenidos.
    tweet_content = "☁PREVISIÓN METEOROLÓGICA☁\n" \
                    "¡Buenos días! Para hoy se esperan los siguientes datos\n" \
                    "Temperatura mínima: " + str(min) + "ºC \t Temperatura máxima: " + str(max) + "ºC\n" \
                                                                                                  "Sensación térmica: " + str(
        sensacion) + "ºC \t\t Humedad: " + str(humidity) + "%\n" \
                                                           "#weather #weatherforecast"

    # Subir el tweet
    print("[TWEET STATUS]")
    try:
        client.create_tweet(text=tweet_content)
        print("Tweet upload successful.")
        print("\n" + tweet_content)
    except:
        print("The upload failed --> " + tweet_content)

if __name__ == '__main__':
    main()