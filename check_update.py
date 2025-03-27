import os
import requests
import zipfile
import sys
import shutil
import time
import threading
import tkinter as tk
from tkinter import ttk

# URLS donde están alojados los archivos de actualización
VERSION_URL = "https://raw.githubusercontent.com/TomasDRS/software_syg/refs/heads/main/version.txt"
ZIP_URL = "https://github.com/TomasDRS/software_syg/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.txt"
INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))  # Directorio del programa

# Crear ventana de actualización
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
    """Actualiza el texto de la ventana"""
    update_label.config(text=new_text)
    update_window.update()

def update_progress(value, total_size):
    """Actualiza la barra de progreso de forma segura"""
    if total_size > 0:  # Evitar división por cero
        percent = int((value / total_size) * 100)
        progress_bar["value"] = percent
        progress_percent.config(text=f"{percent}%")
    else:
        progress_bar.config(mode="indeterminate")  # Cambia a modo indeterminado si no hay tamaño
        progress_bar.start(10)  # Animación de progreso indefinida

    update_window.update()

def get_remote_version():
    """Obtiene la versión más reciente disponible en el servidor."""
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"Error al obtener la versión remota: {e}")
        return None

def get_local_version():
    """Lee la versión instalada en la computadora."""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0.0"

def download_and_extract():
    """Descarga la actualización y reemplaza los archivos automáticamente."""
    show_update_window()  # Mostrar ventana de actualización
    update_text("Descargando actualización...")

    zip_path = os.path.join(INSTALL_PATH, "update.zip")
    try:
        response = requests.get(ZIP_URL, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))  # Obtener tamaño total del archivo

        if total_size == 0:
            print("⚠️ Advertencia: No se pudo obtener el tamaño del archivo. Se usará progreso indeterminado.")

        downloaded_size = 0
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    update_progress(downloaded_size, total_size)  # Actualizar barra de progreso

        progress_bar.stop()  # Detener barra si estaba en modo indeterminado
        progress_bar.config(mode="determinate", value=100)
        progress_percent.config(text="100%")

        update_text("Descomprimiendo archivos...")

        # Extraer archivos
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extract_path = os.path.join(INSTALL_PATH, "update")
            zip_ref.extractall(extract_path)

        # Buscar la carpeta interna (GitHub ZIP siempre agrega "-main")
        subfolder = os.path.join(extract_path, "software_syg-main")

        update_text("Copiando archivos...")

        # Mover archivos de actualización a la carpeta principal
        if os.path.exists(subfolder):
            for item in os.listdir(subfolder):
                source_path = os.path.join(subfolder, item)
                destination_path = os.path.join(INSTALL_PATH, item)

                if os.path.exists(destination_path):
                    if os.path.isdir(destination_path):
                        shutil.rmtree(destination_path)  # Elimina carpetas antiguas
                    else:
                        os.remove(destination_path)  # Borra archivos antiguos

                shutil.move(source_path, INSTALL_PATH)

        # Eliminar archivos temporales
        os.remove(zip_path)
        shutil.rmtree(extract_path)

        update_text("Actualización completada.")
        time.sleep(2)  # Espera un poco antes de cerrar la ventana
        update_window.destroy()  # Cerrar ventana

        return True

    except Exception as e:
        print(f"Error durante la actualización: {e}")
        update_text(f"Error: {e}")
        time.sleep(3)
        update_window.destroy()
        return False

def check_for_updates():
    """Verifica si hay una nueva versión y la instala sin intervención del usuario."""
    remote_version = get_remote_version()
    local_version = get_local_version()

    print(f"Versión instalada: {local_version}")
    print(f"Versión disponible: {remote_version}")

    if remote_version and remote_version != local_version:
        print("Nueva versión encontrada. Iniciando actualización...")

        if download_and_extract():
            # Guardar la nueva versión en el archivo local
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(remote_version)

            print("Reiniciando el programa...")
            time.sleep(2)  # Espera un poco para evitar errores al cerrar archivos
            os.execv(sys.executable, [sys.executable] + sys.argv)  # Reinicia el programa
    else:
        print("El programa ya está actualizado.")

if __name__ == "__main__":
    # Ejecutar el chequeo de actualizaciones en un hilo separado para evitar congelar la ventana
    thread = threading.Thread(target=check_for_updates)
    thread.start()
    thread.join()  # Espera a que termine la actualización

    print("Iniciando programa principal...")
    import login  # Aquí se ejecuta el programa después de la actualización
