from googletrans import Translator


def translate(text):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='es')
        return translated_text.text
    except Exception as e:
        print("Error occurred:", e)
        return None
