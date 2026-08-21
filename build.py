import os
import subprocess
import customtkinter

print("Iniciando la compilación con PyInstaller...")

# Obtener la ruta de customtkinter para incluir sus assets visuales
ctk_path = os.path.dirname(customtkinter.__file__)

# Comando de PyInstaller
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--windowed", # Esto oculta la consola negra
    "--icon=app_icon.ico",
    "--name=Optimizador_de_Fotos",
    f"--add-data={ctk_path};customtkinter/", 
    "main_app.py"
]

try:
    subprocess.run(cmd, check=True)
    print("¡Compilación exitosa! Tu aplicación se encuentra en la carpeta 'dist/Optimizador_de_Fotos'.")
except subprocess.CalledProcessError as e:
    print(f"Error durante la compilación: {e}")
