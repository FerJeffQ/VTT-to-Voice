# Voice Translator to VTT subtitle files

Voice Translator es un programa en python que utiliza Google Translate y Text-to-Speech (TTS) para traducir y generar archivos de audio a partir de subtítulos en formato VTT.

## Requirements

- Python 3.x
- Python libraries (installed with `pip install -r requirements.txt`):
  - gtts
  - webvtt
  - pydub
  - googletrans==4.0.0-rc1  # Asegura la compatibilidad con la versión actual
  - tqdm

## Installation

1. Clona este repositorio o descarga el código fuente.

```bash
git clone https://github.com/YourUsername/VoiceTranslator.git
cd VoiceTranslator
```

2. Instala las dependencias.

```bash
pip install gtts webvtt pydub googletrans==4.0.0-rc1 tqdm
```

## USO
### Ejecución básica
```bash
python voice_translator.py

```

Esto tomará los subtítulos en inglés del archivo VTT predeterminado, traducirá el texto y generará un archivo de audio en español en la carpeta de salida.

## Contribuciones
Si encuentras algún error o tienes sugerencias para mejorar el programa, ¡no dudes en contribuir !