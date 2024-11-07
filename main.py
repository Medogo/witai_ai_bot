from flask import Flask, request, jsonify
from convertion_audio_to_text import speak_translation
from translation import translate_text
from voice_detection import record_audio
from witai_params import send_to_wit
import Levenshtein

app = Flask(__name__)


def calculate_score(reference_text, user_text):
    # Calculer la similarité entre les textes
    similarity = Levenshtein.ratio(reference_text.lower(), user_text.lower()) * 100
    return round(similarity, 2)


@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Étape 1 : Traduire le texte initial
        text = record_audio()
        if not text:
            return jsonify({"error": "No audio detected or transcription failed"}), 400

        wit_response = send_to_wit(text)
        print("Wit.ai Response:", wit_response)

        target_lang = request.json.get('target_lang', 'sw')
        translation = translate_text(text, target_lang)

        speak_translation(translation, lang=target_lang)

        # Boucle pour répéter jusqu'à atteindre 80% ou plus
        score = 0
        while score < 80:
            # Étape 2 : Demander à l'utilisateur de répéter
            repeat_text = record_audio()
            if not repeat_text:
                return jsonify({"error": "No repeated audio detected"}), 400

            # Étape 3 : Calculer le score
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

            # Informer l'utilisateur et le laisser essayer à nouveau
            return jsonify({
                "translated_text": translation,
                "repeated_text": repeat_text,
                "score": score,
                "message": message,
                "retry": True  # Indique qu'il peut réessayer
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