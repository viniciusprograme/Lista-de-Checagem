from fastapi import FastAPI, Response
from starlette.middleware.wsgi import WSGIMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import app as flask_app_module
import sys
import traceback


# Create the Flask app instance using the existing factory, but guard startup
try:
    flask_app = flask_app_module.create_app()
except Exception:
    # Print full traceback to stderr so hosting logs (Railway) capture it
    print("Failed to create Flask app during import:", file=sys.stderr)
    traceback.print_exc()
    # Create a minimal fallback Flask app that returns 500 on requests
    from flask import Flask

    flask_app = Flask(__name__)

    @flask_app.route("/")
    def startup_error():
        return (
            "Application failed to start. Check server logs for details.",
            500,
        )


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
