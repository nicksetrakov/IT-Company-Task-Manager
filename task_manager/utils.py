import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
]


def get_credentials() -> Credentials | None:
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def create_google_task(task, creds) -> dict:
    service = build("tasks", "v1", credentials=creds)

    task_body = {
        "title": task.name,
        "notes": task.description,
        "due": task.deadline.isoformat(),
    }

    created_task = service.tasks().insert(
        tasklist="@default", body=task_body
    ).execute()

    return created_task


def delete_google_task(task_id, creds) -> None:
    service = build("tasks", "v1", credentials=creds)
    service.tasks().delete(tasklist="@default", task=task_id).execute()


def update_google_task(task_id, updated_task_body, creds) -> dict:
    service = build("tasks", "v1", credentials=creds)
    updated_task = (
        service.tasks()
        .patch(tasklist="@default", task=task_id, body=updated_task_body)
        .execute()
    )
    return updated_task


# It is for future realizations
# def create_event(task, creds):
#     service = build('calendar', 'v3', credentials=creds)
#     event = {
#         'summary': task.name,
#         'description': task.description,
#         'start': {
#             'dateTime': task.deadline.isoformat(),
#             'timeZone': 'UTC',
#         },
#         'end': {
#             'dateTime': (
#             task.deadline + datetime.timedelta(hours=1)
#             ).isoformat(),
#             'timeZone': 'UTC',
#         },
#         'attendees': [{'email': task.assignees.first().email}],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'popup', 'minutes': 60},
#             ],
#         },
#     }
#     event = service.events().insert(
#     calendarId='primary', body=event
#     ).execute()
#     return event
#
# def delete_event(event_id, creds):
#     service = build('calendar', 'v3', credentials=creds)
#     service.events().delete(calendarId='primary', eventId=event_id).execute()
