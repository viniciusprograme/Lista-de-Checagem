from fastapi import FastAPI, Response
from starlette.middleware.wsgi import WSGIMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import app as flask_app_module

# Create the Flask app instance using the existing factory
flask_app = flask_app_module.create_app()

app = FastAPI(title="Checklist ASGI adapter")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


# Mount the existing Flask WSGI app at root
app.mount("/", WSGIMiddleware(flask_app))
