FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
# Сначала зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь сервис (гарантированно попадут alembic.ini, alembic/, entrypoint.sh)
COPY . .

ENV PYTHONUNBUFFERED=1

# На всякий случай ensure exec bit
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
