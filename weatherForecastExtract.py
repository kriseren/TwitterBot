# Importo las dependencias.
import requests
import tokens as tkn

def getWeatherData(ciudad):
    # Creamos un diccionario con los parámetros de la URL.
    parametros={"q":ciudad,
                "units":"metric",
                "APPID":tkn.openWeather_secret}

    # Realizamos la petición, indicando la URL y los parámetros.
    respuesta=requests.get("http://api.openweathermap.org/data/2.5/weather",params=parametros)

    # Si la respuesta devuelve el código de estado 200, no han habido errores.
    if respuesta.status_code == 200:
        # La respuesta json se convierte en un diccionario.
        datos = respuesta.json()

        # Se obtienen los valores del diccionario y se retornan.
        temp = datos["main"]["temp"]
        min = datos["main"]["temp_min"]
        max = datos["main"]["temp_max"]
        media = round((max+min)/2,2)
        humidity = datos["main"]["humidity"]
        weatherData = [min,max,media,humidity,temp]
        return datos
    else:
        print("De esa ciudad no tengo datos.")

if __name__ == '__main__':
    getWeatherData("petrer")