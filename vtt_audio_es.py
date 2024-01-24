from gtts import gTTS
import webvtt
from pydub import AudioSegment
import io
from tqdm import tqdm
from httpcore._exceptions import ReadTimeout

class VoiceTranslator:
    def __init__(self, vtt_file_path, output_path):
        self.vtt = webvtt.read(vtt_file_path)
        self.output_path = output_path
        self.final_audio = AudioSegment.silent(duration=0)

    def translate_and_speak(self, text, lang='es'):
        # Utiliza el texto original sin traducción para generar el segmento de audio.
        tts = gTTS(text=text, lang=lang)

        # Guarda el audio en un objeto BytesIO para poder ser utilizado por Pydub.
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Retorna el audio como un segmento de AudioSegment.
        return AudioSegment.from_file(fp, format="mp3")

    def adjust_audio_speed(self, audio, speed=1.35):
        return audio.speedup(playback_speed=speed)

    def add_silence(self, duration):
        return AudioSegment.silent(duration=duration)

    def process_subtitles(self):
        for caption in tqdm(self.vtt, desc="Procesando subtítulos", unit="subtítulo"): 
            # Utiliza el texto original sin traducción.
            audio = self.translate_and_speak(caption.text)
            
            audio = self.adjust_audio_speed(audio)
            
            start_time = caption.start_in_seconds * 1000
            if len(self.final_audio) < start_time:
                self.final_audio += self.add_silence(start_time - len(self.final_audio))
            
            self.final_audio += audio

    def save_audio(self):
        self.final_audio.export(self.output_path, format='mp3')

if __name__ == "__main__":
    path = '/mnt/c/Users/ferje/Documents/Programming/VTT_to_Voice/'
    vtt_file_path = path + 'src/subtitles-es.vtt'  # Cambia el nombre del archivo a uno con la extensión ".es.vtt" o similar.
    output_path = path + 'output/final_audio_es.mp3'
    
    translator = VoiceTranslator(vtt_file_path, output_path)
    translator.process_subtitles()
    
    translator.save_audio()
