# Инструкция по деплою ITAMHack

## Требования

- Docker и Docker Compose установлены
- Минимум 2GB RAM
- 10GB свободного места на диске

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd ITAMHack
```

### 2. Настройка переменных окружения

```bash
cp env.example .env
```

Отредактируйте `.env` файл и укажите:
- `DB_USER`, `DB_PASSWORD`, `DB_NAME` - данные для PostgreSQL
- `SECRET_KEY` - секретный ключ для JWT (минимум 32 символа)
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота
- `REDIS_PASSWORD` - пароль для Redis (опционально)

### 3. Запуск в продакшене

```bash
docker-compose -f docker-compose.prod.yaml up -d
```

### 4. Проверка статуса

```bash
docker-compose -f docker-compose.prod.yaml ps
```

### 5. Просмотр логов

```bash
# Все сервисы
docker-compose -f docker-compose.prod.yaml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yaml logs -f backend
```

## Структура сервисов

- **backend** (порт 8000) - FastAPI приложение
- **frontend** (порт 80) - React приложение через Nginx
- **postgres** (порт 5432) - База данных PostgreSQL
- **redis** (порт 6379) - Redis для кэширования
- **bot** - Telegram бот

## Обновление приложения

```bash
# Остановить сервисы
docker-compose -f docker-compose.prod.yaml down

# Обновить код
git pull

# Пересобрать и запустить
docker-compose -f docker-compose.prod.yaml up -d --build
```

## Резервное копирование базы данных

```bash
# Создать бэкап
docker-compose -f docker-compose.prod.yaml exec postgres pg_dump -U $DB_USER $DB_NAME > backup.sql

# Восстановить из бэкапа
docker-compose -f docker-compose.prod.yaml exec -T postgres psql -U $DB_USER $DB_NAME < backup.sql
```

## Мониторинг

### Проверка здоровья сервисов

```bash
# Backend
curl http://localhost:8000/docs

# Frontend
curl http://localhost
```

### Логи

```bash
# Последние 100 строк логов
docker-compose -f docker-compose.prod.yaml logs --tail=100

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yaml logs backend
```

## Безопасность

### Рекомендации для продакшена:

1. **Измените все пароли по умолчанию** в `.env`
2. **Используйте сильный SECRET_KEY** (минимум 32 символа)
3. **Настройте файрвол** - не открывайте порты PostgreSQL и Redis наружу
4. **Используйте HTTPS** через reverse proxy (Nginx/Traefik)
5. **Регулярно обновляйте** Docker образы
6. **Настройте мониторинг** и алерты

## Настройка HTTPS (опционально)

Для продакшена рекомендуется использовать reverse proxy с SSL:

1. Установите Nginx или Traefik перед приложением
2. Настройте SSL сертификаты (Let's Encrypt)
3. Обновите `API_URL` в `.env` на HTTPS адрес

## Troubleshooting

### Проблема: Сервисы не запускаются

```bash
# Проверьте логи
docker-compose -f docker-compose.prod.yaml logs

# Проверьте статус
docker-compose -f docker-compose.prod.yaml ps
```

### Проблема: База данных не подключается

```bash
# Проверьте переменные окружения
docker-compose -f docker-compose.prod.yaml exec backend env | grep DATABASE

# Проверьте подключение к БД
docker-compose -f docker-compose.prod.yaml exec postgres psql -U $DB_USER -d $DB_NAME
```

### Проблема: Фронтенд не работает

```bash
# Проверьте логи фронтенда
docker-compose -f docker-compose.prod.yaml logs frontend

# Проверьте, что бэкенд доступен
curl http://localhost:8000/docs
```

## Остановка приложения

```bash
# Остановить без удаления данных
docker-compose -f docker-compose.prod.yaml stop

# Остановить и удалить контейнеры (данные сохранятся в volumes)
docker-compose -f docker-compose.prod.yaml down

# Остановить и удалить все включая volumes (ОСТОРОЖНО!)
docker-compose -f docker-compose.prod.yaml down -v
```
