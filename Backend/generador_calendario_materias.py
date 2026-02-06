import sys
import datetime
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse


num_dia = {
    "LUNES": 0,
    "MARTES": 1,
    "MIERCOLES": 2,
    "JUEVES": 3,
    "VIERNES": 4,
    "SABADO": 5,
    "DOMINGO": 6,
}
semanas_cuatrimestre = 16

# Credenciales
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account_file.json" #Archivo no incluido en github

def main():
    if len(sys.argv) < 3:
        print("No se especifico archivo")
        print("Formato: programa.py input.json output.json")
        return
    
    print("Se requiere la fecha del domingo anterior al inicio de dictado de clases.")
    inicio_ano = int(input("Ingrese el año (YYYY): "))
    inicio_mes = int(input("Ingrese el mes (1-12): "))
    inicio_dia = int(input("Ingrese el dia (1-31): "))
    inicio_clases = datetime.date(inicio_ano, inicio_mes, inicio_dia)
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)

    with open(sys.argv[1], 'r', encoding='utf-8') as lectura:
        file_data = json.load(lectura)

    if Path(sys.argv[2]).is_file():
        print("Archivo existente, se retomara la operacion")
        with open(sys.argv[2], 'r', encoding='utf-8') as lectura:
            output_data = json.load(lectura)
    else:
        print("Archivo inexistente, se creara uno nuevo")
        output_data = {}
    try:
        for carrera in file_data:
            if not (carrera in output_data):
                print(f"Generando carrera [{carrera}]")
                output_data[carrera] = {}
            for materia in file_data[carrera]:
                if not (materia in output_data[carrera]):
                    print(f"Generando materia [{carrera}]")
                    output_data[carrera][materia] = {}
                for horario in file_data[carrera][materia]["horarios"]:

                    # Si no existe la comision, se crea su calendario
                    if not (horario["comision"] in output_data[carrera][materia]):
                        print(f'Generando Calendario {materia} {horario["comision"]}')
                        cuerpo_calendario = {
                            "summary": f"{materia} {horario["comision"]}",
                            "timeZone": "America/Argentina/Buenos_Aires"
                        }
                        nuevo_calendario = service.calendars().insert(body=cuerpo_calendario).execute()
                        calendar_id = nuevo_calendario["id"]
                        encoded_calendar_id = urllib.parse.quote(calendar_id)
                        output_data[carrera][materia][horario["comision"]] = {
                            "id": calendar_id,
                            "link": f"https://calendar.google.com/calendar/embed?src={encoded_calendar_id}&ctz=America/Argentina/Buenos_Aires"
                            }
                        print(f'    ID {calendar_id}')
                        # Se hace publico para que se pueda compartir el link
                        acl_rule = {
                            "scope": {
                                "type": "default"  # 'default' engloba a todo usuario
                            },
                            "role": "reader"  # Le da permisos de lectura a todos los usuarios
                        }
                        public_rule = service.acl().insert(calendarId=calendar_id, body=acl_rule).execute()

                        for clase in file_data[carrera][materia]["horarios"]:
                            if clase["comision"] == horario["comision"]:
                                # Creacion de Eventos
                                print(f'Generando Evento {materia} {clase["comision"]} {clase["dia"]}')
                                fecha_inicio = next_weekday(inicio_clases, num_dia[clase["dia"]])
                                nuevo_evento = {
                                    "summary": materia,
                                    "description": f"Clase {materia} {clase["comision"]} {clase["dia"]}",
                                    "location": f"{clase["lugar"]} - Aula {clase["aula"]}",
                                    "start": {
                                        "dateTime": f"{fecha_inicio}T{clase["inicio"]}:00",
                                        "timeZone": "America/Argentina/Buenos_Aires"
                                    },
                                    "end": {
                                        "dateTime": f"{fecha_inicio}T{clase["fin"]}:00",
                                        "timeZone": "America/Argentina/Buenos_Aires"
                                    },
                                    'recurrence': [
                                        f'RRULE:FREQ=WEEKLY;COUNT={semanas_cuatrimestre}'
                                    ],
                                    "reminders": {
                                        "useDefault": True
                                    }
                                }
                                # Agrega el evento al calendario
                                event = service.events().insert(
                                    calendarId=output_data[carrera][materia][clase["comision"]]["id"], body=nuevo_evento).execute()
    except Exception as e:
        print("No se pudo terminar la generacion de calendarios")
        print(e)
    else:
        print("Generacion de calendarios terminada")
    finally:
        with open(sys.argv[2], "w", encoding='utf-8') as outfile:
            json.dump(output_data, outfile, indent=2, ensure_ascii=False)
    # FIN


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

if __name__ == "__main__":
    main()