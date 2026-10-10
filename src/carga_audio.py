"""Lectura de audios: busca los archivos en data/, pasa a mono y remuestrea."""
from math import gcd

import soundfile as sf
from scipy.signal import resample_poly

import config as cfg


def listar_audios():
    """{instrumento: ruta}. Acepta data/flauta.wav o data/flauta/nota.wav."""
    audios = {}
    if not cfg.DATA.exists():
        return audios
    for p in sorted(cfg.DATA.iterdir()):
        if p.is_file() and p.suffix.lower() in cfg.EXTENSIONES:
            audios[p.stem] = p
        elif p.is_dir():
            fs_ = sorted(f for f in p.rglob("*") if f.suffix.lower() in cfg.EXTENSIONES)
            if fs_:
                audios[p.name] = fs_[0]
    return audios


def info_audio(ruta):
    """Parametros originales del archivo (fs, canales, duracion)."""
    return sf.info(str(ruta))


def cargar(ruta):
    """Lee el audio, lo pasa a mono (el timbre no depende del canal) y lo lleva a cfg.FS."""
    x, fs = sf.read(str(ruta), dtype="float64", always_2d=True)
    x = x.mean(axis=1)
    if fs != cfg.FS:
        g = gcd(int(fs), cfg.FS)
        x = resample_poly(x, cfg.FS // g, int(fs) // g)   # incluye filtro antialiasing
    return x
