import os
import requests
import zipfile
import sys
import shutil
import time

# URLS donde están alojados los archivos de actualización
VERSION_URL = "https://raw.githubusercontent.com/TomasDRS/software_syg/refs/heads/main/version.txt"
ZIP_URL = "https://github.com/usuario/repositorio/archive/refs/heads/main.zip"

LOCAL_VERSION_FILE = "version.txt"
INSTALL_PATH = os.path.dirname(os.path.abspath(__file__))  # Directorio del programa

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
    print("Descargando actualización...")

    zip_path = os.path.join(INSTALL_PATH, "update.zip")
    try:
        response = requests.get(ZIP_URL, stream=True)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Descomprimiendo archivos...")

        # Extraer archivos
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            extract_path = os.path.join(INSTALL_PATH, "update")
            zip_ref.extractall(extract_path)

        # Mover archivos de actualización a la carpeta principal
        for item in os.listdir(extract_path):
            source_path = os.path.join(extract_path, item)
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

        print("Actualización completada.")
        return True

    except Exception as e:
        print(f"Error durante la actualización: {e}")
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
    check_for_updates()
    print("Iniciando programa principal...")
    import login  # Aquí se ejecuta el programa después de la actualización