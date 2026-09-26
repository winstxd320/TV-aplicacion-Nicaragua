import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# UBICACIÓN DE LOS ARCHIVOS DE VLC
# ============================================================

if getattr(sys, "frozen", False):
    # Cuando se ejecuta como EXE de PyInstaller
    BASE_DIR = sys._MEIPASS
else:
    # Cuando se ejecuta como archivo .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


VLC_DIR = BASE_DIR
VLC_PLUGINS = os.path.join(VLC_DIR, "plugins")


# ============================================================
# AGREGAR LAS DLL DE VLC AL PATH
# ============================================================

os.environ["PATH"] = VLC_DIR + os.pathsep + os.environ.get("PATH", "")


# Python 3.8+
if hasattr(os, "add_dll_directory"):
    try:
        os.add_dll_directory(VLC_DIR)
    except Exception:
        pass


# ============================================================
# IMPORTAR VLC
# ============================================================

import vlc


# ============================================================
# CREAR INSTANCIA DE VLC
# ============================================================

instance = vlc.Instance(
    f"--plugin-path={VLC_PLUGINS}"
)

player = instance.media_player_new()


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

root = tk.Tk()

root.title("TV Nicaragua")

root.geometry("1000x700")

root.minsize(700, 500)

root.resizable(True, True)


# ============================================================
# ICONO
# ============================================================

icon_path = os.path.join(BASE_DIR, "icono.ico")

try:
    root.iconbitmap(icon_path)
except Exception:
    pass


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    root,
    text="TV Nicaragua",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=10)


# ============================================================
# CANALES
# ============================================================

canales = {

    "Canal 4":
        "https://live.eu-north-1b.cf.dmcdn.net/sec2(LeiD601niGIlqgke1uK1FOVZ6i3XLH4_pK5xuq044lMYQZZTl8l-jQZNrX4JqxwIdyepniZxQYXfyevLdk_5D0Il_VwrdaRsALXQrnu6rmSKuGtYYpKEUGIR0xdLbiz8)/dm/3/x7rwv8c/s/live-480.m3u8",

    "Canal 10":
        "https://d82p4jax9pjrm.cloudfront.net/medialist_4276517416086298479_hls.m3u8",

    "Canal 13":
        "https://cdn.vivamediosni.com/viva_720p/main_stream.m3u8",

    "Canal 6":
        "https://live.eu-north-1b.cf.dmcdn.net/sec2(qdKS96a5c4-Iz2NXvtUUTcLROIZG6R7ielr_F0kXjixRbKRx83A-XfwU8ezzFgYSoQGlpZmrZCv7MQlB-QSXqk42rkiEcNW9gJ4-m6dbcKdknNB_Qo8n1CxG_8TOnbFk)/dm/3/xaka1oy/d/live-480.m3u8?startdate=2026-09-01T17%3A42%3A51%2B0000",

    "Canal 8":
        "https://5ca3e84a76d30.streamlock.net/tn8/videotn8/chunklist_w701471701.m3u8"
}


# ============================================================
# SELECTOR DE CANALES
# ============================================================

selector = ttk.Combobox(
    root,
    values=list(canales.keys()),
    state="readonly",
    font=("Arial", 12)
)

selector.set("Seleccione un canal")

selector.pack(pady=5)


# ============================================================
# ÁREA DE VIDEO
# ============================================================

video_frame = tk.Frame(
    root,
    bg="black"
)

video_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# REPRODUCIR
# ============================================================

def reproducir():

    canal = selector.get()

    if canal not in canales:

        messagebox.showwarning(
            "TV Nicaragua",
            "Seleccione un canal."
        )

        return

    url = canales[canal]

    try:

        # Detener reproducción anterior
        player.stop()

        # Crear medio
        media = instance.media_new(url)

        # Asignar medio
        player.set_media(media)

        # Actualizar ventana
        video_frame.update_idletasks()

        # Colocar video dentro de Tkinter
        player.set_hwnd(
            video_frame.winfo_id()
        )

        # Reproducir
        player.play()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo reproducir el canal.\n\n{e}"
        )


# ============================================================
# PAUSAR
# ============================================================

def pausar():

    try:

        player.pause()

    except Exception:
        pass


# ============================================================
# DETENER
# ============================================================

def detener():

    try:

        player.stop()

    except Exception:
        pass


# ============================================================
# BOTONES
# ============================================================

botones = tk.Frame(root)

botones.pack(pady=10)


# Botón reproducir

btn_reproducir = tk.Button(
    botones,
    text="▶ Reproducir",
    command=reproducir,
    width=15,
    font=("Arial", 11)
)

btn_reproducir.pack(
    side=tk.LEFT,
    padx=5
)


# Botón pausar

btn_pausar = tk.Button(
    botones,
    text="⏸ Pausar",
    command=pausar,
    width=15,
    font=("Arial", 11)
)

btn_pausar.pack(
    side=tk.LEFT,
    padx=5
)


# Botón detener

btn_detener = tk.Button(
    botones,
    text="⏹ Detener",
    command=detener,
    width=15,
    font=("Arial", 11)
)

btn_detener.pack(
    side=tk.LEFT,
    padx=5
)


# ============================================================
# CERRAR VLC CORRECTAMENTE
# ============================================================

def cerrar():

    try:

        player.stop()

        player.release()

        instance.release()

    except Exception:
        pass

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    cerrar
)


# ============================================================
# INICIAR PROGRAMA
# ============================================================

root.mainloop()

