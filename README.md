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

## Run with Helm locally

Start Docker Desktop and its Kubernetes cluster. Install Helm,
then build the local image:

```bash
docker build -t incident-response-lab:local .
```

### First-time migration from the plain Kubernetes files

If the Deployment and Service were previously created using `k8s/`,
remove them before the first Helm installation. This briefly stops
the local API:

```bash
kubectl --context docker-desktop delete -f k8s/ --ignore-not-found
```

Do not repeat this cleanup after Helm manages the application.
Use the Helm chart instead of applying the original `k8s/` files.

### Install or update

```bash
helm upgrade --install ir-api ./charts/ir-api --kube-context docker-desktop --wait --timeout 2m
```

Settings are in `charts/ir-api/values.yaml`.

### Access the API

```bash
kubectl --context docker-desktop port-forward service/ir-api 8001:8000
```

Open http://127.0.0.1:8001/docs.
Press Control+C to stop forwarding.

### View history and roll back

```bash
helm history ir-api --kube-context docker-desktop
```

To restore revision 1, if it appears in the history:

```bash
helm rollback ir-api 1 --kube-context docker-desktop --wait --timeout 2m
```

Rollback creates a new release revision. It does not change local
files; update values.yaml separately to reflect the intended settings.

### Remove the Helm release

```bash
helm uninstall ir-api --kube-context docker-desktop
```

## Deploy with Argo CD locally

The local lab now uses Argo CD to manage the API.
Do not separately run Helm upgrades or apply the original `k8s/`
files to the same application.

### First-time Argo CD installation

Create a namespace for Argo CD:

```bash
kubectl --context docker-desktop create namespace argocd
```

Install its components:

```bash
kubectl --context docker-desktop apply -n argocd --server-side -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This URL follows Argo CD's stable branch; its contents can change.

Check startup:

```bash
kubectl --context docker-desktop get pods -n argocd
kubectl --context docker-desktop -n argocd rollout status deployment/argocd-server --timeout=120s
```

Use the dashboard port-forward command below to open Argo CD.
The local dashboard may show a self-signed certificate warning.

Log in as `admin`. Retrieve the initial password locally:

```bash
kubectl --context docker-desktop -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 --decode; echo
```

Do not commit the password to Git.

### One-time handoff from Helm

Create the Argo CD Application using the settings below, with
Manual sync. Before its first sync, remove the existing Helm
release if it still manages this app:

```bash
helm uninstall ir-api --kube-context docker-desktop
```

This briefly removes the API Deployment and Service.
Then sync the Application in Argo CD to recreate them.

This handoff has already been completed in our local lab.

### Application settings

In Argo CD, create an Application with:

- Name: `ir-api`
- Project: `default`
- Sync policy: Manual
- Repository: `https://github.com/Jbritt23/incident-response-lab.git`
- Revision: `main`
- Path: `charts/ir-api`
- Destination cluster: `https://kubernetes.default.svc`
- Destination namespace: `default`

Argo CD uses Helm to render the chart, then manages the generated
Kubernetes resources. It does not create a Helm release.

The local image must already be available to the Kubernetes node
because the chart uses `imagePullPolicy: Never`.

### Open the Argo CD dashboard

With Docker Desktop and the local cluster running:

```bash
kubectl --context docker-desktop -n argocd port-forward service/argocd-server 8080:443
```

Open https://localhost:8080 and keep this terminal running.

### Deploy a configuration change

1. Create a Git branch and edit the chart settings.
2. Commit, push, and merge a pull request into `main`.
3. Refresh the Application in Argo CD.
4. Review the difference, then select Sync and Synchronize.
5. Confirm the Application is Synced and Healthy.
6. Check the running resources:

```bash
kubectl --context docker-desktop get pods -l app=ir-api
```

Manual sync means merging a pull request does not automatically
deploy it.

### Access the API

In a separate terminal:

```bash
kubectl --context docker-desktop port-forward service/ir-api 8001:8000
```

Open http://127.0.0.1:8001/docs.

Stopping either port-forward closes that tunnel; it does not stop
Argo CD or the API.

## Terraform local practice

This exercise manages one local text file. It does not use AWS.

From the repository root, initialize Terraform:

```bash
terraform -chdir=terraform/local init
```

Preview the changes:

```bash
terraform -chdir=terraform/local plan
```

Create the file after reviewing the plan and entering `yes`:

```bash
terraform -chdir=terraform/local apply
```

The generated file is `terraform/local/lab-note.txt`.

Run plan again to confirm there are no changes:

```bash
terraform -chdir=terraform/local plan
```

Preview cleanup, then remove the managed file:

```bash
terraform -chdir=terraform/local plan -destroy
terraform -chdir=terraform/local destroy
```

Review the destruction plan before entering `yes`.

Commit the `.tf` configuration and `.terraform.lock.hcl`.
Keep Terraform state, downloaded providers, and the generated
text file out of Git.