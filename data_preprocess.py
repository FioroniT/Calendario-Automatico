import pandas as pd
import json
import unicodedata

# ========== AUX ==========#
def limpiar_texto(texto):
    """Elimina tildes y caracteres especiales, y normaliza el texto"""
    if pd.isnull(texto):
        return "-"
    texto = unicodedata.normalize('NFD', str(texto))
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto.strip().upper()

def convertir_hora(x):
    """Convierte número tipo 900 o 1130 en formato HH:MM"""
    try:
        x_float = float(x)
        horas = int(x_float // 100)
        minutos = int(x_float % 100)
        return f"{horas:02d}:{minutos:02d}"
    except:
        return '-'

tabla = pd.ExcelFile('[2025] ICOM Horarios 1er cuatrimestre.xlsx')

# ========== Horarios ==========#
df = pd.read_excel(tabla, sheet_name='horarios', skiprows=7)

cols = [limpiar_texto(c) for c in df.columns]
df.columns = cols


df = df[~df['CODIGO'].isin(['CODIGO', '-', None]) & ~df['MATERIA'].isin(['MATERIA', '-', None])]

for col in df.select_dtypes(include=['object']):
    df[col] = df[col].map(limpiar_texto)

cols_nec = ['CODIGO', 'MATERIA', 'TEORIA  /  PRACTICA', 'COM', 'DIA', 'DESDE', 'HASTA', 'DOCENTE', 'EMAIL', 'LUGAR', 'AULA']
df = df[cols_nec]

df['DESDE'] = df['DESDE'].apply(convertir_hora)
df['HASTA'] = df['HASTA'].apply(convertir_hora)

materias = {}
for _, r in df.iterrows():
    key = f"{r['CODIGO']}-{r['MATERIA']}"

    if r['MATERIA'] in ['---', '-', ''] or any(x in r['MATERIA'] for x in ['ANO', 'AÑO']):
        continue

    horario = {
        'tipo': r['TEORIA  /  PRACTICA'] or 'SIN ESPECIFICAR',
        'comision': r['COM'],
        'dia': r['DIA'],
        'inicio': r['DESDE'],
        'fin': r['HASTA'],
        'aula': r['AULA'],
        'lugar': r['LUGAR'],
    }
    docente = r['DOCENTE'] if r['DOCENTE'] not in ['', '-', 'NAN'] else 'SIN ASIGNAR'
    email = r['EMAIL'] if '@' in r['EMAIL'] else '-'
    if key not in materias:
        materias[key] = {'docente': docente, 'email': email, 'horarios': [horario]}
    else:
        materias[key]['horarios'].append(horario)

# ========== Calendario académico ==========#
df_cal = pd.read_excel(tabla, sheet_name='calendario', skiprows=5)


resultado = {'materias': materias}

with open('materias_y_calendario.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)
