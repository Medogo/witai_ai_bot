import speech_recognition as sr

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris.")
        except sr.RequestError as e:
            print(f"Erreur de service : {e}")
