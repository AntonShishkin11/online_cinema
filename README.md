# 🎬 MVP Онлайн-Кинотеатр

- **Backend**: FastAPI + SQLAlchemy + JWT (заглушка)
- **Frontend**: React (Vite)
- **Web-сервер**: Nginx
- **Контейнеризация**: Docker + Docker Compose

---

## 📁 Структура проекта

```
mvp_online_cinema/
├── backend/       # FastAPI-приложение
├── frontend/      # React-приложение (Vite)
├── nginx/         # Конфигурация Nginx
├── docker-compose.yml
└── README.md
```

---

## 🚀 Быстрый старт (через Docker)

> Убедись, что установлен [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)

### 🔧 Шаг 1: Клонируй или распакуй проект

### 🔧 Шаг 2: Запусти проект

```bash
docker-compose up --build
```

Это:
- Соберёт backend (FastAPI)
- Установит frontend-зависимости и соберёт React-приложение
- Поднимет Nginx как единый веб-сервер

---

## 🌐 Доступ

| Компонент      | URL                          |
|----------------|-------------------------------|
| Главная страница (React) | http://localhost           |
| Swagger API (FastAPI)   | http://localhost/api/docs   |
| Пример API              | http://localhost/api/movies |

---

## 🧪 Запуск без Docker (локально)

> Убедись, что у тебя установлен Python 3.11+ и Node.js

### 🐍 Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Доступ: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### ⚛️ Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Доступ: [http://localhost:5173](http://localhost:5173)

---

## 🧾 Пример данных

### Пример фильма:

```json
{
  "id": 1,
  "title": "Матрица",
  "year": 1999,
  "genre": "Фантастика",
  "video_url": "https://example.com/matrix.mp4"
}
```

---

## 📌 План доработок

- Реализовать настоящую авторизацию с JWT
- Подключить PostgreSQL (вместо SQLite)
- Добавить базу данных фильмов
- Подключить внешнее видео-хранилище и CDN
