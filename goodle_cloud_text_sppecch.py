from google.cloud import texttospeech

def synthesize_speech(text, language_code="wo-WO", voice_name="wo-WO-Standard-A", output_file="output.mp3"):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Configurez la voix pour le Wolof
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Paramètres audio
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Synthèse vocale
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Sauvegarder le fichier audio
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {output_file}")

# Utilisez cette fonction avec votre texte
synthesize_speech("Bonjour, je teste la traduction en Wolof.", "wo-WO")
