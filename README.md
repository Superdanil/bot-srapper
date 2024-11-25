# Wikipedia Bot Scrapper

Этот проект представляет собой сервис для парсинга статей с https://ru.wikipedia.org/ с использованием Telegram бота. 
Весь проект разворачивается и запускается с помощью Docker Compose.

## Технологии

- Aiogram (Telegram Bot API)
- Docker и Docker Compose
- PostgreSQL
- SQLAlchemy
- Loguru

## Функциональность

- Получение случайных ссылок из статьи Википедии (без дублирования) по команде /wikilinks. Количество ссылок 
    определяется в .env
- Получение списка ссылок по которым можно перейти от одной статьи до другой по команде /wikipath. Максимальная длина 
    списка определяется в .env
- Хранение информации о запросах пользователей в базе данных
- Команды бота:
  - /start
  - /wikilinks
  - /wikipath
  - /help

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Клонируйте репозиторий:
   ```
   git clone https://gitlab.lc.f-lab.tech/internship1/bot-srapper
   ```

3. Перейдите в директорию проекта:
   ```
   cd bot-wikipedia-scrapper/app
   ```

4. Переименуйте файл `.env.example` в `.env`.

5. В файле `.env` заполните `BOT_TOKEN` вашим токеном Telegram бота.

6. Запустите проект с помощью Docker Compose:
   ```
   docker-compose up -d --build
   ```

7. Начните взаимодействие с ботом, отправив команду `/start` в Telegram.

## Примечания

- Все сервисы проекта автоматически запускаются и настраиваются через Docker Compose.
- База данных PostgreSQL использует Docker volume для сохранения данных между перезапусками.
- Лог ошибок сохраняется в logs/app_log.log

## Остановка и удаление контейнеров

Для остановки и удаления всех контейнеров проекта используйте команду:
```
docker-compose down
```

Если вы хотите также удалить все созданные volumes (включая данные базы данных), используйте:
```
docker-compose down -v
```