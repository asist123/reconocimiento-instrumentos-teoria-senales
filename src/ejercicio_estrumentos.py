import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

FS = 22050          # frecuencia de muestreo (Hz)
DURACION = 1.0      # duracion de cada nota (s)
NOTA = 440.0        # La4, la nota que usamos para comparar instrumentos

INSTRUMENTOS = {
    "flauta":  {"perfil": [1.0, 0.2, 0.05],                  "ataque": 0.08, "caida": 3.0},
    "guitarra": {"perfil": [1.0, 0.7, 0.5, 0.3, 0.2, 0.1],   "ataque": 0.01, "caida": 5.0},
    "violin":  {"perfil": [1.0, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3], "ataque": 0.12, "caida": 1.5},
}