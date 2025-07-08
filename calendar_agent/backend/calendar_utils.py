# backend/calendar_utils.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

load_dotenv()
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

def get_availability():
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return "You're free for the next few hours."
    free_slots = []
    for i in range(len(events) - 1):
        end = events[i]['end']['dateTime']
        start_next = events[i+1]['start']['dateTime']
        free_slots.append(f"Free between {end} and {start_next}")
    return "\n".join(free_slots) or "No events found."

def book_event():
    tz = pytz.timezone('Asia/Kolkata')
    start = tz.localize(datetime.now() + timedelta(minutes=30))
    end = start + timedelta(minutes=30)
    event = {
        'summary': 'AI Booked Meeting',
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"✅ Meeting booked from {start.strftime('%H:%M')} to {end.strftime('%H:%M')}."
