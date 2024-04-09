from PIL import Image, ImageDraw, ImageFont

def generar_imagen_con_texto(imagen_fondo_path, texto):
    """
    Genera una nueva imagen con texto encima de una imagen de fondo.

    Args:
        imagen_fondo_path (str): Ruta de la imagen de fondo.
        texto (str): Texto que se agregará a la imagen.

    Returns:
        None
    """
    # Abrir la imagen de fondo
    imagen_fondo = Image.open(imagen_fondo_path)

    # Crear un objeto ImageDraw para dibujar sobre la imagen
    dibujo = ImageDraw.Draw(imagen_fondo)

    # Establecer la fuente para el texto
    tamano_fuente = 40
    fuente_path = "/usr/share/fonts/truetype/Sahadeva/sahadeva.ttf"
    fuente = ImageFont.truetype(fuente_path, tamano_fuente)

    # Obtener el tamaño del texto
    tamano_texto = dibujo.textsize(texto, font=fuente)

    # Calcular la posición del texto centrado en la imagen
    x = (imagen_fondo.width - tamano_texto[0]) // 2
    y = (imagen_fondo.height - tamano_texto[1]) // 2

    # Dibujar el texto en la imagen
    color_texto = "black"
    dibujo.text((x, y), texto, fill=color_texto, font=fuente)

    # Guardar la imagen con el texto en un nuevo archivo
    imagen_fondo.save("imagen_con_texto.png")

def main():
    """
    Función principal del script.
    """
    # Llamar a la función para generar la imagen con texto sobre la imagen de fondo
    generar_imagen_con_texto("/home/logan/Escritorio/am23_plantilla.png", "¡Texto a agregar encima!")

if __name__ == "__main__":
    main()
