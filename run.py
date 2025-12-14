# run.py
import sys
import io
import os
from pathlib import Path

# Configuration de l'encodage
if sys.platform == "win32":
    # Windows nécessite une configuration spéciale
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Définir la variable d'environnement pour Python
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Lancer le script principal
if __name__ == "__main__":
    from main import main
    main()