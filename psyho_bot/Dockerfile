# Dockerfile для бэкенда
# Используем образ Python
FROM python:3.9-slim
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Копируем все файлы бэкенда
COPY . .
# Запускаем приложение с помощью uvicorn для FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
# Открываем порт для бэкенда
EXPOSE 5000