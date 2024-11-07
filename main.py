from flask import Flask, request, jsonify
from convertion_audio_to_text import speak_translation
from translation import translate_text
from voice_detection import record_audio
from witai_params import send_to_wit
import Levenshtein

app = Flask(__name__)

# Langues disponibles
AVAILABLE_LANGUAGES = {
    "sw": "Swahili",
    "wo": "Wolof",
    "fon": "Fon",
    "en": "Anglais",
    "fr": "Français"
}

def calculate_score(reference_text, user_text):
    similarity = Levenshtein.ratio(reference_text.lower(), user_text.lower()) * 100
    return round(similarity, 2)

@app.route('/available_languages', methods=['GET'])
def available_languages():
    """Retourne les langues disponibles pour la traduction."""
    return jsonify(AVAILABLE_LANGUAGES)


@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Traite l'audio, traduit le texte et évalue la prononciation."""
    try:
        # Étape 1 : Récupérer la langue cible depuis la requête
        target_lang = request.json.get('target_lang')

        if not target_lang:
            return jsonify({"error": "Paramètre 'target_lang' manquant"}), 400

        if target_lang not in AVAILABLE_LANGUAGES:
            return jsonify({
                "error": f"Langue cible '{target_lang}' non supportée.",
                "available_languages": AVAILABLE_LANGUAGES  # Retourner la liste des langues disponibles
            }), 400

        # Étape 2 : Traduire le texte initial
        text = record_audio()
        if not text:
            return jsonify({"error": "No audio detected or transcription failed"}), 400

        wit_response = send_to_wit(text)
        print("Wit.ai Response:", wit_response)

        translation = translate_text(text, target_lang)
        speak_translation(translation, lang=target_lang)

        # Étape 3 : Boucle de répétition pour évaluer la prononciation
        score = 0
        while score < 80:
            repeat_text = record_audio()
            if not repeat_text:
                return jsonify({"error": "No repeated audio detected"}), 400

            score = calculate_score(translation, repeat_text)
            if score >= 80:
                message = "Bravo! Félicitations, vous êtes un génie!"
                return jsonify({
                    "original_text": text,
                    "wit_response": wit_response,
                    "translated_text": translation,
                    "repeated_text": repeat_text,
                    "score": score,
                    "message": message
                }), 200
            elif score < 45:
                message = "Votre score est faible, améliorez-vous en vous entraînant."
            else:
                message = "Pas mal! Vous pouvez encore améliorer."

            return jsonify({
                "translated_text": translation,
                "repeated_text": repeat_text,
                "score": score,
                "message": message,
                "retry": True
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


"""
tu peux tester avec ce code dans le navigateur, tu decommente, puis tu le met la ou il faut
@app.route('/process_audio', methods=['GET', 'POST'])
def process_audio():
    if request.method == 'GET':
        return jsonify({"message": "Utilisez une requête POST pour traiter l'audio."})
    
    # Continue avec la logique POST
    try:
        text = record_audio()
        if not text:
            return jsonify({"error": "No audio detected or transcription failed"}), 400

        wit_response = send_to_wit(text)
        print("Wit.ai Response:", wit_response)

        target_lang = request.json.get('target_lang', 'sw')
        translation = translate_text(text, target_lang)

        speak_translation(translation, lang=target_lang)

        return jsonify({
            "original_text": text,
            "wit_response": wit_response,
            "translated_text": translation
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""