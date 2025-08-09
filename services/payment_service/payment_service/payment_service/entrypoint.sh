#!/usr/bin/env sh
set -e

# Wait for DB (use SYNC_DATABASE_URL or fallback by stripping "+asyncpg")
python - <<'PY'
import os, time, asyncio, asyncpg

def to_sync_url(url: str) -> str:
    return url.replace("postgresql+asyncpg", "postgresql") if url else url

async def ping():
    url = os.environ.get("SYNC_DATABASE_URL") or to_sync_url(os.environ.get("DATABASE_URL"))
    if not url:
        raise SystemExit("No SYNC_DATABASE_URL or DATABASE_URL provided")

    for i in range(30):
        try:
            conn = await asyncpg.connect(dsn=url)
            await conn.close()
            print("DB is up")
            return
        except Exception as e:
            print("DB not ready, retrying...", e)
            await asyncio.sleep(1)
    raise SystemExit("DB did not become ready in time")

asyncio.run(ping())
PY

# Run migrations (DATABASE_URL остаётся async: postgresql+asyncpg, как нужно Alembic-у в async env.py)
# Run migrations
alembic -c /app/alembic.ini upgrade head


# Start API
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
