
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.api.internal import router as internal_router
from app.database import init_db
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Subscription Service", version="1.0.0")

app.include_router(api_router, prefix="/api/v1/subscription", tags=["subscription"])
app.include_router(internal_router, prefix="/internal/subscription", tags=["internal"])

@app.on_event("startup")
async def on_startup():
    # Ensure DB is reachable; tables created via Alembic, not here.
    await init_db()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path_item in openapi_schema.get("paths", {}).values():
        for op in path_item.values():
            if isinstance(op, dict):
                op.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
