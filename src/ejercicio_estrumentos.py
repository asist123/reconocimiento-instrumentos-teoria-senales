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

def generar_nota(instrumento, f0=NOTA, fs=FS, dur=DURACION):
    """Crea una nota sumando armonicos y aplicando una envolvente."""
    t = np.arange(int(fs * dur)) / fs
    p = INSTRUMENTOS[instrumento]
    x = np.zeros_like(t)
    for k, a in enumerate(p["perfil"], start=1):
        x += a * np.sin(2 * np.pi * k * f0 * t)
 
    # envolvente: sube en el ataque y luego decae exponencialmente
    env = np.minimum(t / p["ataque"], 1.0) * np.exp(-p["caida"] * t / dur)
    x = x * env
    return t, x / np.max(np.abs(x))
 
 
def cargar_wav(ruta):
    """Para cuando ya tengamos audios reales (.wav). Devuelve (fs, senal)."""
    fs, x = wavfile.read(ruta)
    if x.ndim > 1:                       # si es estereo, pasar a mono
        x = x.mean(axis=1)
    x = x.astype(float)
    return fs, x / np.max(np.abs(x))

def grafica_tiempo():
    fig, ejes = plt.subplots(len(INSTRUMENTOS), 1, figsize=(9, 6), sharex=True)
    for ax, nombre in zip(ejes, INSTRUMENTOS):
        t, x = generar_nota(nombre)
        ax.plot(t, x, linewidth=0.6)
        ax.set_ylabel(nombre)
        ax.grid(alpha=0.3)
    ejes[0].set_title("Misma nota (440 Hz) en distintos instrumentos")
    ejes[-1].set_xlabel("Tiempo (s)")
    plt.tight_layout()