import subprocess
import os

# Cambia al directorio donde está tu archivo
ruta_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_script)

# Ejecuta Streamlit
subprocess.call('start cmd /k "streamlit run Simulador_ahorro.py"', shell=True)
