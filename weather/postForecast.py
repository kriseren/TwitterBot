from auth import auth_utilities
import weatherForecastExtract


#Autenticación en twitter.
client = utilities.authenticateToTwitter()

#Obtención de datos meteorológicos.
weatherData = weatherForecastExtract.getWeatherData("petrer")
min = weatherData["main"]["temp_min"]
max = weatherData["main"]["temp_max"]
media = min+max/2
humidity = weatherData["main"]["humidity"]
temp = weatherData["main"]["temp"]
sensacion = weatherData["main"]["feels_like"]

#Creación del tweet con los datos obtenidos.
tweet_content = "☁PREVISIÓN METEOROLÓGICA☁\n" \
                "¡Buenos días! Para hoy se esperan los siguientes datos\n" \
                "Temperatura mínima: "+str(min)+"ºC \t Temperatura máxima: "+str(max)+"ºC\n" \
                "Sensación térmica: "+str(sensacion)+"ºC \t\t Humedad: "+str(humidity)+"%\n" \
                "#weather #weatherforecast"

#Upload the tweet
print("[TWEET STATUS]")
try:
    #client.create_tweet(text=tweet_content)
    print("Tweet upload successful.")
    print("\n"+tweet_content)
except:
    print("The upload failed --> "+tweet_content)