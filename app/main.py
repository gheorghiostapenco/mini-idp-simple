from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Mini IDP v0 – YAML Generator")

templates = Jinja2Templates(directory="app/templates")

# Если потом захочешь CSS/JS – можно подключить static
# app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Show the main form for environment parameters.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    service_name: str = Form(...),
    env_type: str = Form("dev"),
    replicas: int = Form(1),
):
    """
    Generate a multi-document YAML with Namespace, Deployment, Service and Ingress.
    """
    service_name = service_name.strip()
    env_type = env_type.strip()
    env_name = f"{service_name}-{env_type}"

    yaml_text = f"""apiVersion: v1
kind: Namespace
metadata:
  name: {env_name}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: {env_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
    spec:
      containers:
        - name: {service_name}
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: {env_name}
spec:
  selector:
    app: {service_name}
  ports:
    - name: http
      port: 80
      targetPort: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {service_name}
  namespace: {env_name}
spec:
  rules:
    - host: {env_name}.apps.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {service_name}
                port:
                  number: 80
"""

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "env_name": env_name,
            "yaml_text": yaml_text,
        },
    )
