# Admin Service

## Запуск

```bash
docker build -t admin_service .
docker run -p 8002:8000 admin_service
```

## Авторизация в Swagger

1. Нажмите **Authorize**
2. Введите:

```
Bearer admin_token
```

или

```
Bearer moderator_token
```