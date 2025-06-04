import pandas as pd
import json
import os

# Directorio con los archivos JSON
directorio = "Outputs\\tmp"

# Diccionario para almacenar todos los JSON
resultado_final = {}

# Leer todos los archivos JSON del directorio
for i, archivo in enumerate(os.listdir(directorio)):
    if archivo.endswith('.json'):
        ruta_completa = os.path.join(directorio, archivo)
        df = pd.read_json(ruta_completa)
        datos_json = df.to_dict()
        resultado_final[archivo] = datos_json

with open("Outputs\\merge_carreras.json", 'w', encoding='utf-8') as f:
    json.dump(resultado_final, f, indent=4, ensure_ascii=False)