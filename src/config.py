"""Parametros y rutas del proyecto. Todo se ajusta desde aqui."""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent if AQUI.name == "src" else AQUI
DATA = RAIZ / "data"
RESULTS = RAIZ / "results"

EXTENSIONES = (".wav", ".mp3", ".flac", ".ogg")   # WAV es el formato principal
FS = 44100          # Hz: todos los audios se llevan a esta frecuencia de muestreo
DURACION = 1.0      # s: segmento de analisis (igual para todos los instrumentos)
OFFSET_ATAQUE = 0.05  # s despues del inicio de la nota
UMBRAL_ONSET = 0.10   # fraccion del RMS maximo que marca el inicio de la nota
SNRS = [20, 5]      # dB: niveles de ruido gaussiano
SEMILLA = 42        # reproducibilidad del ruido
F_MAX_GRAFICA = 5000  # Hz: limite del eje de frecuencia en las figuras
