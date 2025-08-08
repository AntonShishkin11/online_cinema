from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1 import films_b2c, users

app = FastAPI(title="Admin Service")

# Роутеры
app.include_router(films_b2c.router, prefix="/admin/films/b2c", tags=["Films B2C"])
app.include_router(users.router,     prefix="/admin",            tags=["Users"])

# Кастомный OpenAPI — показываем в Swagger именно Bearer-авторизацию
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Admin Service API",
        routes=app.routes,
    )
    comps = openapi_schema.setdefault("components", {})
    comps["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # По умолчанию требуем Bearer для всех ручек (если для какой-то не нужно — убери вручную)
    for path in openapi_schema.get("paths", {}).values():
        for op in path.values():
            op.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
