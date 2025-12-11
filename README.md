# Mini IDP v0 – Kubernetes Environment YAML Generator

A tiny **Internal Developer Platform (IDP) prototype** that generates
Kubernetes manifests for application environments via a simple web UI.

Instead of provisioning namespaces and workloads automatically,
this first version focuses on **standardizing golden-path YAML** for developers:

- Developer fills a small form (service name, environment type, replicas).
- The app generates a single multi-document YAML including:
  - `Namespace`
  - `Deployment`
  - `Service`
  - `Ingress`
- Developer can copy or download the YAML and apply it manually:

```bash
kubectl apply -f env.yaml
```

This is the minimal but realistic starting point for a future Mini IDP
with GitOps, Argo CD integration, TTL-based cleanup and self-service previews.

**Features (v0)**

Web form for creating a simple environment definition:

service_name (e.g. billing-service)
env_type (dev, preview, etc.)
replicas (1–5)

Generated Kubernetes manifests:

Isolated Namespace per environment
Basic Deployment (default image: nginx:alpine for demo)
Service (ClusterIP)
Ingress with a per-environment hostname (e.g. billing-dev.apps.example.com)

All logic in a small Python backend (FastAPI/Flask style).

Tech stack (planned)

Backend: Python 3.11+, FastAPI (or Flask)
Templating: Jinja2 (for HTML pages)
Runtime: Uvicorn / Gunicorn inside Docker
Kubernetes: any cluster (k3s, k3d, kind, managed cloud, etc.)

Project structure (planned)

mini-idp-simple/
  app/
    main.py            # FastAPI/Flask entrypoint
    templates/
      index.html       # Form for input
      result.html      # Page showing generated YAML
  tests/
  Dockerfile
  requirements.txt
  README.md

Quickstart (local development)

Note: commands are examples, adjust paths/names as needed.

# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app (FastAPI example)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Usage example

1. Open the main page.
2. Enter:

service_name: billing-service
env_type: dev
replicas: 2

3. Click Generate.

4. Copy the YAML into a file:


---

## Architecture / How it works

This project is intentionally small, but it models a real Internal Developer Platform flow:

1. **Developer UI**  
   A simple HTML form served by FastAPI:
   - `service_name` (e.g. `billing-service`)
   - `env_type` (e.g. `dev`, `preview`)
   - `replicas` (number of pod replicas)

2. **Backend logic (Mini IDP brain)**  
   The backend receives the form data and generates a **multi-document Kubernetes YAML**:
   - `Namespace` – isolated per environment (`<service>-<env>`).
   - `Deployment` – simple web workload (default `nginx:alpine` image).
   - `Service` – ClusterIP service exposing the pod.
   - `Ingress` – HTTP routing with a per-environment hostname.

3. **Manual apply (v0)**  
   In this first version, developers:
   - copy the YAML from the UI,
   - save it as `env.yaml`,
   - apply it manually:

   ```bash
   kubectl apply -f env.yaml



This is effectively a tiny, opinionated golden-path generator for Kubernetes environments.
The same pattern can be extended later with:

GitOps (commit generated manifests into a config repo),

Argo CD / Flux for automatic sync,

TTL and automatic cleanup of preview environments,

authentication and per-team templates.


## Why this is a Mini IDP (and not just a toy)

Even though the implementation is small, this project demonstrates key
Internal Developer Platform concepts:

- **Golden path templates**  
  Developers don't have to remember all the details of Kubernetes manifests.
  They just provide high-level parameters, and the platform generates
  a consistent, production-like environment definition.

- **Separation of concerns**  
  - Developers focus on the service name and basic scaling.
  - The platform owns the Kubernetes details (namespaces, services, ingress).

- **Ready for GitOps**  
  The YAML generator can be the first step towards:
  - committing manifests into a Git repository,
  - using Argo CD / Flux to reconcile the desired state,
  - implementing preview environments for pull requests.

- **Clear roadmap**  
  This v0 is intentionally minimal, but it has a realistic path to:
  - self-service environments,
  - multi-tenant platform behaviour,
  - cost and lifecycle controls (TTL, auto-cleanup),
  - security guardrails baked into the templates.