from gtts import gTTS
import playsound
import os

def speak_translation(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "translation.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
