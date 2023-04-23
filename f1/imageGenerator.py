from PIL import Image, ImageDraw, ImageFont

# Función para generar la imagen con texto encima de una imagen existente
def generar_imagen_con_texto(imagen_fondo, texto):
    # Abrir la imagen de fondo
    fondo = Image.open(imagen_fondo)

    # Crear un objeto ImageDraw para dibujar sobre la imagen
    dibujo = ImageDraw.Draw(fondo)

    # Establecer la fuente para el texto
    tamano_fuente = 40
    fuente = ImageFont.truetype("/usr/share/fonts/truetype/Sahadeva/sahadeva.ttf", tamano_fuente)

    # Obtener el tamaño del texto
    tamano_texto = dibujo.textsize(texto, font=fuente)

    # Calcular la posición del texto centrado en la imagen
    x = (fondo.width - tamano_texto[0]) // 2
    y = (fondo.height - tamano_texto[1]) // 2

    # Dibujar el texto en la imagen
    dibujo.text((x, y), texto, fill="black", font=fuente)

    # Guardar la imagen con el texto en un nuevo archivo
    fondo.save("ej1.png")

# Llamar a la función para generar la imagen con texto sobre la imagen de fondo
generar_imagen_con_texto("/home/logan/Escritorio/am23_plantilla.png", "¡Texto a agregar encima!")
