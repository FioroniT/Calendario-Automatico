import pandas as pd
import unicodedata
import re
import json
import os

def procesar_excel_a_json(archivo_excel):
    df = pd.read_excel(archivo_excel, header=None, skiprows=7)
    materias_dict = {}
    anio_actual = None
    materia_actual = None
    clave_actual = None
    for idx, fila in enumerate(df.itertuples(index=False), 1):
        celdas = []
        for x in fila:
            if pd.isna(x) or x is None or str(x).strip() in ["", "nan"]:
                celdas.append(None)
            else:
                celdas.append(str(x).strip())
        celdas += [None] * (11 - len(celdas))
        a, b, c, d, e, f, g, h, i, j, k = celdas[:11]
        if a and "AÑO" in a:
            anio_actual = a
            continue
        
        if a and a.startswith("MATERIA"):
            continue

        if a and a != "nan":
            materia_actual = a
            clave_actual = materia_actual.replace(" - ", "-").upper()
            
            if clave_actual not in materias_dict:
                materias_dict[clave_actual] = {
                    "docente": "-",
                    "email": "-",
                    "horarios": []
                }

        if materia_actual and d and d != "nan":
            norm = unicodedata.normalize('NFKD', d)
            d = ''.join([c for c in norm if not unicodedata.combining(c)])
            d.upper()
            comision = "C1"
            if d:
                if d == "MIÉRCOLES":
                    d = "MIERCOLES"
            if c:
                match = re.search(r'C\d+', c)
                if match:
                    comision = match.group(0)
            tipo_clase = "CLASE"
            if c:
                c_lower = c.lower()
                if "teór" in c_lower or "teor" in c_lower or "teoria" in c_lower:
                    tipo_clase = "TEORIA"
                elif "práct" in c_lower or "pract" in c_lower or "prac" in c_lower:
                    tipo_clase = "PRACTICA"
                elif "teor/pract" in c_lower or "teórico/práctico" in c_lower:
                    tipo_clase = "TEORICO/PRACTICO"
            inicio, fin = None, None
            if g:
                if " a " in g:
                    horario_parts = g.split(" a ")
                elif " - " in g:
                    horario_parts = g.split(" - ")
                else:
                    horario_parts = [g]
                if len(horario_parts) == 2:
                    inicio = horario_parts[0].strip()
                    fin = horario_parts[1].strip()
                elif len(horario_parts) == 1:
                    inicio = fin = horario_parts[0].strip()
            horario_data = {
                "tipo": tipo_clase if tipo_clase else "-",
                "comision": comision if comision else "-",
                "dia": d.upper() if d else "-",
                "inicio": inicio if inicio else "-",
                "fin": fin if fin else "-",
                "aula": f if f else "-",
                "lugar": e if e else "-"
            }
            materias_dict[clave_actual]["horarios"].append(horario_data)
            if i and i != "nan" and not materias_dict[clave_actual]["docente"]:
                docente = re.split(r'[/,]', i)[0].strip().upper()
                materias_dict[clave_actual]["docente"] = docente
    
    return json.dumps(materias_dict, indent=2, ensure_ascii=False)

for entry in os.scandir('Inputs'):  
    if entry.is_file() and entry.path.endswith(".xlsx"):
        json_str = procesar_excel_a_json(entry.path)
        materias = json.loads(json_str)
        with open(f'Outputs\\tmp\\{entry.path.split('\\')[1]}.json', 'w', encoding='utf-8') as f:
            json.dump(materias, f, indent=2, ensure_ascii=False)