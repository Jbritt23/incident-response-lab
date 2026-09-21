# Incident Response Lab

A learning project for building and deploying an AI-assisted
incident response application.

## Learning goals

- Python
- AWS: EC2, IAM, EKS, and Bedrock
- Docker and Kubernetes
- Terraform, Helm, and Argo CD
- Workflow orchestration with n8n and LangGraph
- Prompt engineering, AI agents, and MCP integrations

## Run locally on macOS

Use Python 3.13. Run these commands from the repository folder.

### Create a virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the tests

```bash
python -m unittest -v
```

### Start the API

```bash
python -m uvicorn api:app --reload
```

Keep the server running and open http://127.0.0.1:8000/docs
in your browser to try the endpoints.

Press Control+C in the terminal to stop the server.

### Analyze login events

Send a POST request to `/analyze` with a JSON body such as:

```json
[
  {"event": "login_failed"},
  {"event": "login_success"},
  {"event": "login_failed"}
]
```

Expected response:

```json
{"failed_logins": 2}
```

Each record must contain an `event` field with a text value.
A record missing that field receives a 422 validation response.