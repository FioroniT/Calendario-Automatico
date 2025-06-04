import sys
import datetime
import json
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
inicio_clases = datetime.date(2025, 3, 2)
semanas_cuatrimestre = 16
#fin_clases = datetime.date(2025, 6, 21)

# Credenciales
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account_file.json" #Archivo no incluido en github

def main():
    if len(sys.argv) < 2:
        print("No se especifico archivo")
        return
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("calendar", "v3", credentials=creds)

    with open(sys.argv[1], 'r', encoding='utf-8') as lectura:
        file_data = json.load(lectura)
    
    # carrera = os.path.basename(sys.argv[1]).split('.')[0]

    prueba_contar = 4

    output_data = {}
    for carrera in file_data:
        output_data[carrera] = {}
        if prueba_contar < 0:
            break
        for materia in file_data[carrera]:
            prueba_contar = prueba_contar - 1
            if prueba_contar < 0:
                break

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
                            "type": "default"  # 'default' means public for anyone.
                        },
                        "role": "reader"  # This grants read-only access to anyone.
                    }
                    public_rule = service.acl().insert(calendarId=calendar_id, body=acl_rule).execute()

                # Creacion de Eventos
                print(f'Generando Evento {materia} {horario["comision"]} {horario["dia"]}')
                fecha_inicio = next_weekday(inicio_clases, num_dia[horario["dia"]])
                nuevo_evento = {
                    "summary": materia,
                    "description": f"Clase {materia} {horario["comision"]} {horario["dia"]}",
                    "location": f"{horario["lugar"]} - Aula {horario["aula"]}",
                    "start": {
                        "dateTime": f"{fecha_inicio}T{horario["inicio"]}:00",
                        "timeZone": "America/Argentina/Buenos_Aires"
                    },
                    "end": {
                        "dateTime": f"{fecha_inicio}T{horario["fin"]}:00",
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
                    calendarId=output_data[carrera][materia][horario["comision"]]["id"], body=nuevo_evento).execute()

    with open("links.json", "w", encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=2, ensure_ascii=False)
    # FIN


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

if __name__ == "__main__":
    main()