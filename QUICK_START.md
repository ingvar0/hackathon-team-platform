# Быстрый старт для деплоя

## 1. Подготовка

```bash
# Скопируйте пример переменных окружения
cp env.example .env

# Отредактируйте .env - обязательно укажите:
# - DB_USER, DB_PASSWORD, DB_NAME
# - SECRET_KEY (минимум 32 символа)
# - TELEGRAM_BOT_TOKEN
```

## 2. Запуск

```bash
# Запуск в продакшене
docker-compose -f docker-compose.prod.yaml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yaml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yaml logs -f
```

## 3. Проверка

- Frontend: http://localhost (или ваш домен)
- Backend API: http://localhost:8000/docs
- API через фронтенд: http://localhost/docs

## 4. Остановка

```bash
docker-compose -f docker-compose.prod.yaml down
```

Подробная документация: [DEPLOY.md](./DEPLOY.md)
