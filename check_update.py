import os
import requests
import zipfile
import sys
import shutil
import time
import threading
import tkinter as tk
from tkinter import ttk

# Detectar si estamos ejecutando como .exe
if getattr(sys, 'frozen', False):
    INSTALL_PATH = os.path.dirname(sys.executable)  # Para .exe
else:
    INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))  # Para script .py

VERSION_URL = "https://raw.githubusercontent.com/TomasDRS/software_syg/refs/heads/main/version.txt"
ZIP_URL = "https://github.com/TomasDRS/software_syg/archive/refs/heads/main.zip"
LOCAL_VERSION_FILE = os.path.join(INSTALL_PATH, "version.txt")

# GUI de actualización
def show_update_window():
    global update_label, update_window, progress_bar, progress_percent
    update_window = tk.Tk()
    update_window.title("Actualización en progreso")
    update_window.geometry("400x180")
    update_window.resizable(False, False)

    tk.Label(update_window, text="Actualizando software...", font=("Arial", 12, "bold")).pack(pady=10)

    update_label = tk.Label(update_window, text="Descargando actualización...", font=("Arial", 10))
    update_label.pack(pady=5)

    progress_bar = ttk.Progressbar(update_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)

    progress_percent = tk.Label(update_window, text="0%", font=("Arial", 10))
    progress_percent.pack(pady=5)

    update_window.update()

def update_text(new_text):
    update_label.config(text=new_text)
    update_window.update()

def update_progress(value, total_size):
    if total_size > 0:
        percent = int((value / total_size) * 100)
        progress_bar["value"] = percent
        progress_percent.config(text=f"{percent}%")
    else:
        progress_bar.config(mode="indeterminate")
        progress_bar.start(10)
    update_window.update()

def get_remote_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"Error al obtener la versión remota: {e}")
        return None

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"

def download_and_extract():
    show_update_window()
    update_text("Descargando actualización...")

    zip_path = os.path.join(INSTALL_PATH, "update.zip")
    try:
        response = requests.get(ZIP_URL, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        if total_size == 0:
            print("⚠️ Advertencia: No se pudo obtener el tamaño del archivo. Se usará progreso indeterminado.")

        downloaded_size = 0
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    update_progress(downloaded_size, total_size)

        if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
            print("Error: La descarga falló.")
            return False

        progress_bar.stop()
        progress_bar.config(mode="determinate", value=100)
        progress_percent.config(text="100%")

        update_text("Descomprimiendo archivos...")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extract_path = os.path.join(INSTALL_PATH, "update")
            zip_ref.extractall(extract_path)

        subfolder = os.path.join(extract_path, "software_syg-main")  # Cambia este nombre si es diferente

        update_text("Copiando archivos...")

        if os.path.exists(subfolder):
            # Mover archivos extraídos directamente al directorio de instalación
            for item in os.listdir(subfolder):
                source_path = os.path.join(subfolder, item)
                destination_path = os.path.join(INSTALL_PATH, item)

                if os.path.exists(destination_path):
                    if os.path.isdir(destination_path):
                        shutil.rmtree(destination_path)  # Eliminar directorios anteriores
                    else:
                        os.remove(destination_path)  # Eliminar archivos anteriores

                shutil.move(source_path, INSTALL_PATH)

        os.remove(zip_path)  # Eliminar archivo ZIP descargado
        shutil.rmtree(extract_path)  # Eliminar carpeta temporal

        update_text("Actualización completada.")
        time.sleep(2)
        update_window.destroy()

        return True

    except Exception as e:
        print(f"Error durante la actualización: {e}")
        update_text(f"Error: {e}")
        input("Presiona ENTER para salir...")  # Evita que la ventana se cierre inmediatamente
        update_window.destroy()
        return False

def check_for_updates():
    remote_version = get_remote_version()
    local_version = get_local_version()

    print(f"Versión instalada: {local_version}")
    print(f"Versión disponible: {remote_version}")

    if remote_version and remote_version != local_version:
        print("Nueva versión encontrada. Iniciando actualización...")

        if download_and_extract():
            # Actualizar el archivo version.txt
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(remote_version)

            print("Reiniciando el programa...")
            time.sleep(2)
            os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        print("El programa ya está actualizado.")

if __name__ == "__main__":
    thread = threading.Thread(target=check_for_updates)
    thread.start()
    thread.join()

    print("Iniciando programa principal...")
    import login
