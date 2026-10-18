import os
import sys


def resource_path(relative_path):
    # Si c'est l'exe PyInstaller, les fichiers sont dans _MEIPASS (le dossier _internal)
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    # Sinon (en script), on prend le dossier du projet
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)