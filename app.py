from flask import Flask, render_template, request, jsonify, send_file, url_for
from ibm_watson import LanguageTranslatorV3, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

app = Flask(__name__)

#Language Translator
lt_api_key = os.getenv('lt_api_key')
lt_url = os.getenv('lt_url')
lt_authenticator = IAMAuthenticator(lt_api_key)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=lt_authenticator)
lt.set_service_url(lt_url)

#TextToSpeech
tts_api_key = os.getenv('tts_api_key')
tts_url = os.getenv('tts_url')
tts_authenticator = IAMAuthenticator(tts_api_key)
tts = TextToSpeechV1(authenticator=tts_authenticator)
tts.set_service_url(tts_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.json['text']
        from_language = request.json['from_language']
        to_language = request.json['to_language']


        translation = lt.translate(text=text, source=from_language, target=to_language).get_result()
        translated_text = translation['translations'][0]['translation']

        
        voices = tts.list_voices().get_result()
        voice_model = None

        # Search for a voice that matches the "to language" based on a substring match
        for voice in voices['voices']:
            if voice['language'].startswith(to_language):
                voice_model = voice['name']
                break

        if voice_model is None:
            voice_model = 'en-US_EmilyV3Voice'

        pronunciation = tts.synthesize(translated_text, accept='audio/mp3', voice=voice_model).get_result()
        audio_filename = 'pronunciation.mp3'

        # Save the audio to a temporary file
        with open(audio_filename, 'wb') as audio_file:
            audio_file.write(pronunciation.content)

        # Construct the response
        response = {
            'translation': translated_text,
            'pronunciation_url': url_for('get_audio', filename=audio_filename)
        }
        return jsonify(response)
    except Exception as e:
        # Log and handle the error
        print(f'Error: {str(e)}')
        return jsonify({'error': 'An error occurred during translation.'}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
