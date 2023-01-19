# API-сервис хранилища событий

## Документация API (Swagger)

1. API доступно по api `/api/v1/openapi`

## Первый запуск

1. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
3. Запустить докер `docker compose up -d --build`

## Первый локальный запуск

1. Сформировать виртуальное Python-окружение `python -m venv venv`
2. Установить зависимости `pip install -r requirements.txt`
3. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
4. Добавить дополнительный файл `docker-compose.dev.yml`, в котором открыть порт для `kafka`
5. Запустить zookeeper и kafka `docker compose -f docker-compose.yml -f docker-compose.dev.yml up zookeeper kafka -d`
6. Перейти в папку с приложением `cd src/app`
7. Запустить приложение `python app.py`

## Линтер

Запуск: `flake8 src/`