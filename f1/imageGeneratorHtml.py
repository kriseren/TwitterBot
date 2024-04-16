import asyncio
import requests
from utilities.TelegramService import send_telegram_message
import auth.tokens as tkn
from auth import auth_utilities


def main(client):
    """
    Función principal del script.

    Lee el contenido de los archivos HTML y CSS, y envía una solicitud POST
    a la API de HCTI para generar una imagen con el contenido HTML y CSS proporcionado.
    Publica un tweet en Twitter con la imagen generada.
    """
    # Leer el contenido del archivo HTML
    with open("facts/factTemplate.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Leer el contenido del archivo CSS
    with open("facts/factTemplate.css", "r", encoding="utf-8") as file:
        css_content = file.read()

    # Definir el tamaño de la imagen
    image_width = 700
    image_height = 1000

    # Parámetros de la solicitud a la API de HCTI
    data = {
        'html': html_content,
        'css': css_content,
        'viewport_width': image_width,
        'viewport_height': image_height
    }

    # Realizar la solicitud a la API de HCTI
    image_response = requests.post(url=tkn.hcti_api_endpoint, data=data, auth=(tkn.hcti_api_user_id, tkn.hcti_api_key))

    # Verificar el resultado de la solicitud
    if image_response.status_code == 200:
        image_url = image_response.json()['url']
        print("Image URL:", image_url)

        # Enviar la imagen por telegram.
        asyncio.run(send_telegram_message(chat_id=tkn.telegram_admin_chat_id, message="PRUEBA PRUEBITA PRUEBA", photo_path=image_url))
    else:
        print("Failed to create image. Error:", image_response.text)


if __name__ == "__main__":
    # Autenticar al cliente de Twitter
    client = auth_utilities.authenticate_to_twitter()
    main(client)
