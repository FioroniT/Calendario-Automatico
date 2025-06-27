import sys
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

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

    #Crear calendario
    print("Generando calendario")
    cuerpo_calendario = {
        "summary": "Calendario Academico UNRN",
        "timeZone": "America/Argentina/Buenos_Aires"
    }
    nuevo_calendario = service.calendars().insert(body=cuerpo_calendario).execute()
    calendar_id = nuevo_calendario["id"]
    encoded_calendar_id = urllib.parse.quote(calendar_id)
    print(f'Generado calendario con ID {calendar_id}')
    acl_rule = { "scope": { "type": "default" }, "role": "reader" }
    public_rule = service.acl().insert(calendarId=calendar_id, body=acl_rule).execute()

    output_data = {"link": f"https://calendar.google.com/calendar/embed?src={encoded_calendar_id}&ctz=America/Argentina/Buenos_Aires"}
    with open("link_calendario_academico.json", "w", encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=2, ensure_ascii=False)

    # Creacion de Eventos
    for fecha in file_data:
        print(f'Generando evento de fecha {fecha}: {file_data[fecha]}')
        nuevo_evento = {
            "summary": file_data[fecha],
            #"description": "Evento universitario",
            "start": {
                "date": fecha,
                "timeZone": "America/Argentina/Buenos_Aires"
            },
            "end": {
                "date": fecha,
                "timeZone": "America/Argentina/Buenos_Aires"
            },
            "reminders": {
                "useDefault": True
            }
        }
        # Agrega el evento al calendario
        event = service.events().insert(
            calendarId=calendar_id, body=nuevo_evento).execute()

if __name__ == "__main__":
    main()