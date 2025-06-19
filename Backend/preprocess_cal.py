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
    if pd.isna(date_str) or not str(date_str).strip():
        return []

    date_str = str(date_str).strip()

    if ' al ' in date_str or ' a ' in date_str or '-' in date_str:
        for sep in [' al ', ' a ', '-']:
            if sep in date_str:
                parts = date_str.split(sep, 1)
                try:
                    start_date = pd.to_datetime(parts[0].strip(), dayfirst=True).date()
                    end_date = pd.to_datetime(parts[1].strip(), dayfirst=True).date()
                    return pd.date_range(start_date, end_date).date.tolist()
                except:
                    continue

    if ' y ' in date_str and any(m in date_str.lower() for m in MESES):
        parts = re.split(r'\s+y\s+', date_str, flags=re.IGNORECASE)
        dates = []
        for part in parts:
            match = re.search(r'(\d{1,2})\s+de\s+(\w+)', part, flags=re.IGNORECASE)
            if match:
                day = int(match.group(1))
                month = match.group(2).lower()
                if month in MESES:
                    dates.append(datetime.date(default_year, MESES[month], day))
        return dates

    match = re.search(r'(\d{1,2})?\s*de?\s*(\w+)', date_str, flags=re.IGNORECASE)
    if match:
        day = int(match.group(1)) if match.group(1) else 1
        month = match.group(2).lower()
        if month in MESES:
            return [datetime.date(default_year, MESES[month], day)]

    try:
        return [pd.to_datetime(date_str, dayfirst=True).date()]
    except:
        return []

# === EXTRACCIÓN PDF === #
tablas = []

with pdfplumber.open('Inputs\\calendario_academico.pdf') as pdf:
    for i in range(2, 13):
        pagina = pdf.pages[i]
        tablas_en_pagina = pagina.extract_tables()
        for tabla in tablas_en_pagina:
            filas = tabla[1:]  # Excluye encabezados
            tablas.extend(filas)

df = pd.DataFrame(tablas).dropna(axis=1, how='all')

if len(df.columns) == 4:
    df.columns = ['idx', 'fecha', 'evento1', 'evento2']
    df = df[['fecha', 'evento1', 'evento2']]
elif len(df.columns) == 3:
    df.columns = ['fecha', 'evento1', 'evento2']
else:
    raise ValueError(f"Estructura inesperada: {len(df.columns)} columnas")

feriados_mask = df.index.isin(range(126, 154)) | df.index.isin(range(170, 173))
df['motivo'] = df['evento1']
df.loc[feriados_mask, 'motivo'] = df.loc[feriados_mask, 'evento2']

df = df[df['fecha'].notna() & df['motivo'].notna() & (df['motivo'] != '')]
df['fechas'] = df['fecha'].apply(parse_date_string)
df = df.explode('fechas').dropna(subset=['fechas'])

df['fecha_iso'] = df['fechas'].apply(lambda d: d.strftime('%Y-%m-%d'))

# === NUEVO AGRUPAMIENTO: BLOQUES CONSECUTIVOS POR MOTIVO === #
df = df.sort_values(by='fecha_iso').reset_index(drop=True)

df['prev_fecha'] = df['fecha_iso'].shift()
df['prev_motivo'] = df['motivo'].shift()

def is_new_group(row):
    if pd.isna(row['prev_fecha']) or pd.isna(row['prev_motivo']):
        return True
    prev_date = datetime.datetime.strptime(row['prev_fecha'], '%Y-%m-%d').date()
    curr_date = datetime.datetime.strptime(row['fecha_iso'], '%Y-%m-%d').date()
    return (curr_date - prev_date).days > 1 or row['motivo'] != row['prev_motivo']

df['new_group'] = df.apply(is_new_group, axis=1)
df['group_id'] = df['new_group'].cumsum()


min_max = df.groupby('motivo')['fecha_iso'].agg(['min', 'max']).reset_index() # Obtener solo inicio y fin de cada grupo

result = {}
for _, row in min_max.iterrows():
    result[row['min']] = row['motivo']
    if row['max'] != row['min']:
        result[row['max']] = row['motivo']

result = dict(sorted(result.items(), key=lambda x: x[0]))

# === EXPORTACIÓN FINAL === #
with open('Outputs\\calendario_academico.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Exportación completa con eventos consolidados.")
