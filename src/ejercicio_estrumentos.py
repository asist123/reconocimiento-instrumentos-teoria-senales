# Reconocimiento de instrumentos musicales con analisis espectral (Teoria General de Senales)
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

FS = 22050
DURACION = 1.0
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CARPETA = os.path.join(RAIZ, "data")
RESULTADOS = os.path.join(RAIZ, "results")


def cargar_audios():
    audios = {}
    for archivo in sorted(os.listdir(CARPETA)):
        nombre, ext = os.path.splitext(archivo)
        if ext.lower() != ".wav":
            print(f"Se omite {archivo}: hay que convertirlo a .wav")
            continue
        fs, x = wavfile.read(os.path.join(CARPETA, archivo))
        x = x.astype(float)
        if x.ndim > 1:
            x = x.mean(axis=1)
        if fs != FS:
            x = signal.resample_poly(x, FS, fs)
        x = x[:int(DURACION * FS)]
        audios[nombre] = x / np.max(np.abs(x))
    return audios


AUDIOS = cargar_audios()


def guardar(nombre):
    os.makedirs(RESULTADOS, exist_ok=True)
    ruta = os.path.join(RESULTADOS, nombre + ".png")
    plt.savefig(ruta, dpi=150)
    print(f"Imagen guardada en {os.path.normpath(ruta)}")


def grafica_tiempo():
    fig, ejes = plt.subplots(len(AUDIOS), 1, figsize=(9, 1.4 * len(AUDIOS)), sharex=True)
    for ax, (nombre, x) in zip(ejes, AUDIOS.items()):
        ax.plot(np.arange(len(x)) / FS, x, linewidth=0.6)
        ax.set_ylabel(nombre, rotation=0, ha="right")
        ax.grid(alpha=0.3)
    ejes[0].set_title("Senal de cada instrumento en el tiempo")
    ejes[-1].set_xlabel("Tiempo (s)")
    plt.tight_layout()
    guardar("grafica_tiempo")


def grafica_muestreo():
    x = AUDIOS["guitarra"]
    t = np.arange(len(x)) / FS
    ini = int(0.2 * FS)
    fin = ini + 600
    fs_bajas = [FS, 4000, 1500]
    fig, ejes = plt.subplots(len(fs_bajas), 1, figsize=(9, 6), sharex=True)
    for ax, fs_nuevo in zip(ejes, fs_bajas):
        paso = int(FS / fs_nuevo)
        ax.plot(t[ini:fin], x[ini:fin], color="lightgray", label="original")
        ax.stem(t[ini:fin:paso], x[ini:fin:paso], linefmt="C1-", markerfmt="C1o",
                basefmt=" ", label=f"fs = {fs_nuevo} Hz")
        ax.legend(loc="upper right")
        ax.grid(alpha=0.3)
    ejes[0].set_title("Efecto de la frecuencia de muestreo (guitarra)")
    ejes[-1].set_xlabel("Tiempo (s)")
    plt.tight_layout()
    guardar("grafica_muestreo")


def espectro(x, fs=FS):
    ventana = np.hanning(len(x))
    X = np.abs(np.fft.rfft(x * ventana))
    f = np.fft.rfftfreq(len(x), 1 / fs)
    return f, X / np.max(X)


def frecuencia_fundamental(x, fs=FS):
    f, X = espectro(x, fs)
    return f[np.argmax(X)]


def grafica_espectro():
    fig, ejes = plt.subplots(len(AUDIOS), 1, figsize=(9, 1.4 * len(AUDIOS)), sharex=True)
    for ax, (nombre, x) in zip(ejes, AUDIOS.items()):
        f, X = espectro(x)
        ax.plot(f, X)
        ax.set_xlim(0, 4000)
        ax.set_ylabel(nombre, rotation=0, ha="right")
        ax.grid(alpha=0.3)
        print(f"{nombre}: pico principal en {frecuencia_fundamental(x):.1f} Hz")
    ejes[0].set_title("Espectro de cada instrumento")
    ejes[-1].set_xlabel("Frecuencia (Hz)")
    plt.tight_layout()
    guardar("grafica_espectro")


def agregar_ruido_awgn(x, snr_db, rng=None):
    # Ruido blanco gaussiano con potencia Pn = Ps / 10^(SNR/10)
    rng = np.random.default_rng() if rng is None else rng
    potencia_senal = np.mean(x ** 2)
    potencia_ruido = potencia_senal / 10 ** (snr_db / 10)
    return x + rng.normal(0, np.sqrt(potencia_ruido), len(x))


def grafica_ruido(instrumento="guitarra", snr_db=15):
    x = AUDIOS[instrumento]
    rng = np.random.default_rng(0)
    y = agregar_ruido_awgn(x, snr_db, rng)

    snr_medida = 10 * np.log10(np.mean(x ** 2) / np.mean((y - x) ** 2))
    print(f"{instrumento}: SNR objetivo = {snr_db} dB, SNR medida = {snr_medida:.2f} dB")
    print(f"Pico principal limpio: {frecuencia_fundamental(x):.1f} Hz, "
          f"con ruido: {frecuencia_fundamental(y):.1f} Hz")

    t = np.arange(len(x)) / FS
    ini = int(0.2 * FS)
    fin = ini + 600
    f, Xl = espectro(x)
    _, Xr = espectro(y)

    fig, ejes = plt.subplots(2, 1, figsize=(9, 7))
    ejes[0].plot(t[ini:fin], y[ini:fin], color="C1", linewidth=0.8, label=f"con ruido (SNR = {snr_db} dB)")
    ejes[0].plot(t[ini:fin], x[ini:fin], color="C0", linewidth=1.2, label="limpia")
    ejes[0].set_title(f"Degradacion por ruido AWGN ({instrumento})")
    ejes[0].set_xlabel("Tiempo (s)")
    ejes[0].set_ylabel("Amplitud")
    ejes[0].legend(loc="upper right")
    ejes[0].grid(alpha=0.3)

    ejes[1].plot(f, 20 * np.log10(Xr + 1e-12), color="C1", linewidth=0.6, label="con ruido")
    ejes[1].plot(f, 20 * np.log10(Xl + 1e-12), color="C0", linewidth=0.8, label="limpia")
    ejes[1].set_xlim(0, 5000)
    ejes[1].set_ylim(-100, 5)
    ejes[1].set_title("Espectro (escala dB)")
    ejes[1].set_xlabel("Frecuencia (Hz)")
    ejes[1].set_ylabel("Magnitud (dB)")
    ejes[1].legend(loc="upper right")
    ejes[1].grid(alpha=0.3)
    plt.tight_layout()
    guardar("grafica_ruido")


def menu():
    opciones = {
        "1": ("Senal en el tiempo", grafica_tiempo),
        "2": ("Muestreo", grafica_muestreo),
        "3": ("Espectro (FFT)", grafica_espectro),
        "4": ("Analisis de Ruido / Degradacion", grafica_ruido),
    }
    while True:
        print("\n--- Reconocimiento de instrumentos ---")
        for clave, (nombre, _) in opciones.items():
            print(f"{clave}. {nombre}")
        print("0. Salir")
        eleccion = input("Elige una opcion: ").strip()

        if eleccion == "0":
            break
        if eleccion in opciones:
            opciones[eleccion][1]()
            plt.show()
        else:
            print("Opcion no valida")


if __name__ == "__main__":
    menu()