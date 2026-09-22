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

## Run with Docker

Start Docker Desktop, then run these commands from the repository folder.

### Build the image

```bash
docker build -t incident-response-lab:local .
```

### Start the container

```bash
docker run --rm --name ir-lab -p 127.0.0.1:8000:8000 incident-response-lab:local
```

Open http://127.0.0.1:8000/docs to try the API.

Press Control+C in the terminal to stop the container.
The container is removed when it stops; the image remains.

After changing application code or dependencies, rebuild the image
and start a new container to use those changes.

## Run with local Kubernetes

Start Docker Desktop with its Kubernetes cluster enabled.
These instructions use the local `docker-desktop` context.

Build the image:

```bash
docker build -t incident-response-lab:local .
```

The deployment uses `imagePullPolicy: Never`, so the image must
already be available to the Kubernetes node.

Create or update the Deployment and Service:

```bash
kubectl --context docker-desktop apply -f k8s/
```

Check the Pods and Service:

```bash
kubectl --context docker-desktop get pods -l app=ir-api
kubectl --context docker-desktop get service ir-api
```

Connect your Mac to an API Pod selected by the Service:

```bash
kubectl --context docker-desktop port-forward service/ir-api 8001:8000
```

Keep the terminal running and open http://127.0.0.1:8001/docs.

Press Control+C to stop forwarding. The application keeps running
in Kubernetes.

To remove this application's Deployment and Service:

```bash
kubectl --context docker-desktop delete -f k8s/
```