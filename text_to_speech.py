# text_to_speech.py
from google.cloud import texttospeech
import os
import tempfile
import playsound
import threading  # Import threading

class TextToSpeechModule:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, voice_name="en-US-Studio-O", speaking_rate=1.0):
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
        )
        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        return response.audio_content

    def play_audio(self, audio_content):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(audio_content)
            temp_audio_path = temp_audio.name
        try:
            playsound.playsound(temp_audio_path)
        finally:
            os.remove(temp_audio_path)

    def play_audio_async(self, audio_content):
        """Plays audio in a separate thread."""
        thread = threading.Thread(target=self.play_audio, args=(audio_content,))
        thread.start()

    def handle_message(self, message, context):
        text = message.get("content")
        audio = self.synthesize_speech(text)
        if audio:
            self.play_audio_async(audio)  # Play audio asynchronously
            return "Audio Played"
        else:
            return "Audio synthesis failed."