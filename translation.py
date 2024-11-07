from googletrans import Translator

def translate_text(text, target_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        print(f"Traduction : {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Erreur lors de la traduction : {e}")
        return "Traduction non disponible"
