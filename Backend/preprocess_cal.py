import pandas as pd
import pdfplumber
import datetime
import re
import json
MESES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

def parse_date_string(date_str, default_year=2025):
    """Convierte una cadena de fecha en una lista de objetos date"""
    if pd.isna(date_str) or not str(date_str).strip():
        return []
    
    date_str = str(date_str).strip()
    
    if ' al ' in date_str or ' a ' in date_str or '-' in date_str:
        separators = [' al ', ' a ', '-']
        for sep in separators:
            if sep in date_str:
                parts = date_str.split(sep, 1)
                if len(parts) == 2:
                    start_str = parts[0].strip()
                    end_str = parts[1].strip()
                    try:
                        start_date = pd.to_datetime(start_str, dayfirst=True).date()
                        end_date = pd.to_datetime(end_str, dayfirst=True).date()
                        return pd.date_range(start_date, end_date).date.tolist()
                    except:
                        continue
    
    # Manejar múltiples fechas
    if ' y ' in date_str and any(mes in date_str.lower() for mes in MESES):
        parts = re.split(r'\s+y\s+', date_str, flags=re.IGNORECASE)
        dates = []
        for part in parts:
            match = re.search(r'(\d{1,2})\s+de\s+(\w+)', part, flags=re.IGNORECASE)
            if match:
                day = int(match.group(1))
                month_name = match.group(2).lower()
                if month_name in MESES:
                    dates.append(datetime.date(default_year, MESES[month_name], day))
        if dates:
            return dates
    
    # Manejar fechas textuales
    if any(mes in date_str.lower() for mes in MESES):
        match = re.search(r'(\d{1,2})?\s*de?\s*(\w+)', date_str, flags=re.IGNORECASE)
        if match:
            day = int(match.group(1)) if match.group(1) else 1
            month_name = match.group(2).lower()
            if month_name in MESES:
                return [datetime.date(default_year, MESES[month_name], day)]
    try:
        return [pd.to_datetime(date_str, dayfirst=True).date()]
    except:
        return []

tablas = []

with pdfplumber.open('Examples\calendario_academico.pdf') as pdf:
    for i in range(2, 13):  # Páginas 3 a 13
        pagina = pdf.pages[i]
        # Extraer tablas
        tablas_en_pagina = pagina.extract_tables()
        for tabla in tablas_en_pagina:
            encabezados = tabla[0]
            filas = tabla[1:]
            for fila in filas:
                tablas.append(fila)

df = pd.DataFrame(tablas)

df = df.dropna(axis=1, how='all')

if len(df.columns) == 4:
    df.columns = ['idx', 'fecha', 'evento1', 'evento2']
    df = df[['fecha', 'evento1', 'evento2']]
elif len(df.columns) == 3:
    df.columns = ['fecha', 'evento1', 'evento2']
else:
    raise ValueError(f"Estructura inesperada del CSV: {len(df.columns)} columnas")

feriados_mask = df.index.isin(range(126, 154)) | df.index.isin(range(170, 173))
df['motivo'] = df['evento1']
df.loc[feriados_mask, 'motivo'] = df.loc[feriados_mask, 'evento2']

df = df[df['fecha'].notna() & df['motivo'].notna() & (df['motivo'] != '')]

df['fechas'] = df['fecha'].apply(parse_date_string)
df = df.explode('fechas').dropna(subset=['fechas'])

# Formatear fechas como strings ISO
df['fecha_iso'] = df['fechas'].apply(lambda d: d.strftime('%Y-%m-%d'))

result = df.groupby('fecha_iso')['motivo'].agg(lambda x: ' | '.join(x)).to_dict()

with open('Outputs\\calendario_academico.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)