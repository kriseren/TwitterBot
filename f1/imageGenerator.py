from PIL import Image, ImageDraw, ImageFont
import textwrap


def generar_imagen_con_texto(imagen_fondo_path, texto, max_width=40, max_height=10, x_offset=0, y_offset=0):
    """
    Genera una nueva imagen con texto encima de una imagen de fondo.

    Args:
        imagen_fondo_path (str): Ruta de la imagen de fondo.
        texto (str): Texto que se agregará a la imagen.
        max_width (int): Longitud máxima permitida para el texto antes de envolverlo. Por defecto es 40.
        max_height (int): Número máximo de líneas permitidas para el texto antes de cortarlo. Por defecto es 10.
        x_offset (int): Desplazamiento horizontal del texto. Por defecto es 0.
        y_offset (int): Desplazamiento vertical del texto. Por defecto es 0.

    Returns:
        None
    """
    # Abrir la imagen de fondo
    imagen_fondo = Image.open(imagen_fondo_path)

    # Crear un objeto ImageDraw para dibujar sobre la imagen
    dibujo = ImageDraw.Draw(imagen_fondo)

    # Establecer la fuente para el texto
    tamano_fuente = 40
    fuente_path = "facts/fonts/Roboto-Bold.ttf"
    fuente = ImageFont.truetype(fuente_path, tamano_fuente)

    # Obtener el tamaño del texto y envolverlo si excede la longitud máxima
    wrapper = textwrap.TextWrapper(width=max_width)
    texto_envuelto = wrapper.wrap(texto)

    # Limitar el número máximo de líneas permitidas para el texto
    texto_envuelto = texto_envuelto[:max_height]

    # Calcular la posición y el tamaño del área de dibujo para el texto
    area_dibujo = (0, 0, imagen_fondo.width, imagen_fondo.height)
    area_dibujo_texto = (area_dibujo[0] + x_offset, area_dibujo[1] + y_offset, area_dibujo[2], area_dibujo[1] + tamano_fuente * max_height + y_offset)

    # Dibujar el texto en la imagen
    color_texto = "#231c42"
    for linea in texto_envuelto:
        # Obtener el tamaño de la línea de texto
        tamano_texto = dibujo.textsize(linea, font=fuente)
        x = (imagen_fondo.width - tamano_texto[0]) // 2 + x_offset
        dibujo.text((x, area_dibujo_texto[1]), linea, fill=color_texto, font=fuente)
        area_dibujo_texto = (area_dibujo_texto[0], area_dibujo_texto[1] + tamano_fuente, area_dibujo_texto[2], area_dibujo_texto[3])

    # Guardar la imagen con el texto en un nuevo archivo
    imagen_fondo.save("imagen_con_texto.png")


def main(text):
    """
    Función principal del script.
    """
    # Llamar a la función para generar la imagen con texto sobre la imagen de fondo
    generar_imagen_con_texto("/home/logan/Descargas/plantilla.png", text, x_offset=-30, y_offset=300)


if __name__ == "__main__":
    main(text="Hola! Soy KriserenBot y mi creador me está haciendo algunas mejoras...")
