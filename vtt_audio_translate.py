from gtts import gTTS
import webvtt
from pydub import AudioSegment
from googletrans import Translator
import io
from tqdm import tqdm
from httpcore._exceptions import ReadTimeout

class VoiceTranslator:
    def __init__(self, vtt_file_path, output_path):
        # Inicialización de la clase VoiceTranslator con la ruta del archivo VTT y la ruta de salida para el audio.
        self.translator = Translator()
        self.vtt = webvtt.read(vtt_file_path)
        self.output_path = output_path
        self.final_audio = AudioSegment.silent(duration=0)

    def translate_and_speak(self, text, lang='es', max_retries=3):
        # Traduce el texto a otro idioma y lo convierte en un segmento de audio usando Google Text-to-Speech (gTTS).
        translation = self.translator.translate(text, dest=lang)
        tts = gTTS(text=translation.text, lang=lang)

        # Guarda el audio en un objeto BytesIO para poder ser utilizado por Pydub.
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Retorna el audio como un segmento de AudioSegment.
        return AudioSegment.from_file(fp, format="mp3")

    def adjust_audio_speed(self, audio, speed=1.35):
        # Ajusta la velocidad de reproducción del audio.
        return audio.speedup(playback_speed=speed)

    def add_silence(self, duration):
        # Agrega silencio al final del audio para sincronizar los subtítulos correctamente.
        return AudioSegment.silent(duration=duration)

    def process_subtitles(self):
        # Procesa cada subtítulo en el archivo VTT.
        for caption in tqdm(self.vtt, desc="Procesando subtítulos", unit="subtítulo"): 
                    
            # Traduce y convierte el texto del subtítulo en un segmento de audio.
            audio = self.translate_and_speak(caption.text)
            
            # Ajusta la velocidad del audio.
            audio = self.adjust_audio_speed(audio)
            
            # Calcula el tiempo de inicio del subtítulo y agrega silencio si es necesario.
            start_time = caption.start_in_seconds * 1000
            if len(self.final_audio) < start_time:
                self.final_audio += self.add_silence(start_time - len(self.final_audio))
            
            # Agrega el audio traducido al audio final.
            self.final_audio += audio

    def save_audio(self):
        # Guarda el audio final en un archivo MP3 en la ruta especificada.
        self.final_audio.export(self.output_path, format='mp3')
        print('Audio guardado con exito!')

if __name__ == "__main__":
    # Configuración de las rutas de entrada y salida.
    path = '/mnt/c/Users/ferje/Documents/Programming/VTT_to_Voice/'
    vtt_file_path = path + 'src/subtitles-en.vtt'
    output_path = path + 'output/final_audio.mp3'
    
    # Creación de una instancia de VoiceTranslator y ejecución del proceso de traducción.
    translator = VoiceTranslator(vtt_file_path, output_path)
    translator.process_subtitles()
    
    # Guarda el audio final.
    translator.save_audio()
