import tkinter as tk
import numpy as np
import sounddevice as sd

# Parâmetros de áudio
sample_rate = 44100  # Hz
duration = 0.5       # segundos

# Frequências das notas na oitava 4 (base)
NOTE_FREQUENCIES = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
}

WHITE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_NOTES_POS = {"C#": 75, "D#": 175, "F#": 375, "G#": 475, "A#": 575}
KEYBOARD_MAP = {
    "a": "C",  "w": "C#",
    "s": "D",  "e": "D#",
    "d": "E",
    "f": "F",  "t": "F#",
    "g": "G",  "y": "G#",
    "h": "A",  "u": "A#",
    "j": "B"
}

# Oitava atual
oitava = 4
MIN_OITAVA = 2
MAX_OITAVA = 6

def gerar_som_piano(frequency, duration=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Harmônicos simples
    wave = (
        0.6 * np.sin(2 * np.pi * frequency * t) +
        0.3 * np.sin(2 * np.pi * frequency * 2 * t) +
        0.1 * np.sin(2 * np.pi * frequency * 3 * t)
    )
    
    # Envelope (ADSR simplificado)
    attack = int(0.05 * sample_rate)
    decay = int(0.15 * sample_rate)
    sustain_level = 0.6
    release = int(0.2 * sample_rate)
    sustain = len(t) - (attack + decay + release)

    envelope = np.concatenate([
        np.linspace(0, 1, attack),  # attack
        np.linspace(1, sustain_level, decay),  # decay
        np.full(sustain, sustain_level),  # sustain
        np.linspace(sustain_level, 0, release)  # release
    ])

    wave = wave[:len(envelope)] * envelope
    return wave


def get_frequency(note, octave):
    base_freq = NOTE_FREQUENCIES[note]
    return base_freq * (2 ** (octave - 4))

def tocar_nota(nota):
    freq = get_frequency(nota, oitava)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    sd.play(gerar_som_piano(freq), sample_rate)

def tecla_pressionada(event):
    tecla = event.char.lower()
    if tecla == 'z':
        diminuir_oitava()
    elif tecla == 'x':
        aumentar_oitava()
    else:
        nota = KEYBOARD_MAP.get(tecla)
        if nota:
            tocar_nota(nota)

def aumentar_oitava():
    global oitava
    if oitava < MAX_OITAVA:
        oitava += 1
        atualizar_label()

def diminuir_oitava():
    global oitava
    if oitava > MIN_OITAVA:
        oitava -= 1
        atualizar_label()

def atualizar_label():
    label_oitava.config(text=f"Oitava atual: {oitava}")

# Interface
root = tk.Tk()
root.title("Piano Dinâmico")
root.geometry("800x300")
root.configure(bg="black")
root.bind("<Key>", tecla_pressionada)

# Teclas brancas
for i, nota in enumerate(WHITE_NOTES):
    tk.Button(
        root, text=nota, width=10, height=8,
        bg="white", fg="black", font=("Arial", 10, "bold"),
        command=lambda n=nota: tocar_nota(n)
    ).place(x=i*100, y=100)

# Teclas pretas
for nota, x in BLACK_NOTES_POS.items():
    tk.Button(
        root, text=nota, width=5, height=5,
        bg="black", fg="white", font=("Arial", 8, "bold"),
        command=lambda n=nota: tocar_nota(n)
    ).place(x=x, y=100)

# Controles de oitava
tk.Button(root, text="Oitava ↓", command=diminuir_oitava, width=10, height=2).place(x=650, y=10)
tk.Button(root, text="Oitava ↑", command=aumentar_oitava, width=10, height=2).place(x=650, y=60)
label_oitava = tk.Label(root, text=f"Oitava atual: {oitava}", font=("Arial", 12), fg="white", bg="black")
label_oitava.place(x=650, y=110)

root.mainloop()
