# Используем официальный Python образ
FROM python:3.12.2-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем все зависимости из requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Запускаем ваш Telegram-бот
CMD ["python", "levidw.py"]
