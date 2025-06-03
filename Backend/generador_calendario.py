from google.oauth2 import service_account
from googleapiclient.discovery import build
import urllib.parse

# Define the scope and load your service account credentials
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account_file.json" #Archivo no incluido en github

def main():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("calendar", "v3", credentials=creds)

    # Creacion de calendario
    calendar_body = {
        "summary": "Calendario Materia Prueba 2",
        "timeZone": "America/Argentina/Buenos_Aires"
    }

    created_calendar = service.calendars().insert(body=calendar_body).execute()
    calendar_id = created_calendar["id"]
    encoded_calendar_id = urllib.parse.quote(calendar_id)
    subscription_link = f"https://calendar.google.com/calendar/embed?src={encoded_calendar_id}&ctz=America/Argentina/Buenos_Aires"
    print(f"Created calendar with ID: {calendar_id}")

    # Se hace publico para que se pueda compartir el link
    acl_rule = {
        "scope": {
            "type": "default"  # 'default' means public for anyone.
        },
        "role": "reader"  # This grants read-only access to anyone.
    }

    public_rule = service.acl().insert(calendarId=calendar_id, body=acl_rule).execute()
    #print("Calendar is now public:")
    #print(public_rule)

    # Creacion de Eventos
    event_body = {
        "summary": "ClasePrueba2",
        "description": "Descripcion de la clase 2A",
        "location": "Aula1234",
        "start": {
            "dateTime": "2025-06-06T12:00:00",
            "timeZone": "America/Argentina/Buenos_Aires"
        },
        "end": {
            "dateTime": "2025-06-06T13:00:00",
            "timeZone": "America/Argentina/Buenos_Aires"
        },
        "reminders": {
            "useDefault": True
        }
    }

    # Agrega el evento al calendario
    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

    event_body = {
        "summary": "ClasePrueba2",
        "description": "Descripcion de la clase 2B",
        "location": "Aula1234",
        "start": {
            "dateTime": "2025-06-08T14:00:00",
            "timeZone": "America/Argentina/Buenos_Aires"
        },
        "end": {
            "dateTime": "2025-06-08T15:00:00",
            "timeZone": "America/Argentina/Buenos_Aires"
        },
        "reminders": {
            "useDefault": True
        }
    }

    # Agrega el evento al calendario
    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
    print(f"Link para compartir: {subscription_link}")


if __name__ == "__main__":
    main()