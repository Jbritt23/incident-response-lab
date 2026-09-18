from fastapi import FastAPI
from parse_logs import count_failed_logins

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/about")
def about():
    return {"name": "Incident Response Lab"}

@app.post("/analyze")
def analyze(events: list[dict]):
    failed_count = count_failed_logins(events)
    return {"failed_logins": failed_count}