import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

FS = 22050          # frecuencia de muestreo (Hz)
DURACION = 1.0      # duracion de cada nota (s)
NOTA = 440.0        # La4, la nota que usamos para comparar instrumentos

