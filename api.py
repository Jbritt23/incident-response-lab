from fastapi import FastAPI
from parse_logs import count_failed_logins
from pydantic import BaseModel

class LoginEvent(BaseModel):
    event: str

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/about")
def about():
    return {"name": "Incident Response Lab"}

@app.post("/analyze")
def analyze(events: list[LoginEvent]):
    events_dicts =[]

    for event in events:
        events_dicts.append(event.model_dump())

    failed_count = count_failed_logins(events_dicts)
    return {"failed_logins": failed_count}