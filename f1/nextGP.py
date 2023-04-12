from auth import auth_utilities
import datetime

#Definición de variables.
tweet_content = ""

#Autenticación en twitter.
client = utilities.authenticateToTwitter()

# Lee los datos de los Grandes Premios desde el archivo.
with open('grandes_premios.txt', 'r') as f:
    lineas = f.readlines()

# Encuentra el Gran Premio más próximo a la fecha actual
today = datetime.date.today()
gp_cercano = min((linea for linea in lineas if datetime.datetime.strptime(linea.strip().split(', ')[0], '%d-%m-%Y').date() > today), key=lambda linea: datetime.datetime.strptime(linea.strip().split(', ')[0], '%d-%m-%Y').date())

# Calcula cuántos días quedan para el próximo Gran Premio. 
fecha_gp, pais, ciudad, circuito = gp_cercano.strip().split(', ')
dia, mes, anio = fecha_gp.split('-')
fecha_gp = datetime.date(int(anio), int(mes), int(dia))
days_left = (fecha_gp - today).days

# Crea el mensaje del tweet.
tweet_content = f"¡ATENCIÓN FANS DEL NANO!\nQuedan {days_left} días para el Gran Premio de {pais} en {ciudad} - {circuito} 🏎️🏁 \n🏆¿Conseguiremos la 33?🏆\n#{pais.replace(' ', '')}"

#Upload the tweet
print("[TWEET STATUS]")
try:
    client.create_tweet(text=tweet_content)
    print("Tweet upload successful.")
    print("\n"+tweet_content)
except:
    print("The upload failed --> "+tweet_content)
