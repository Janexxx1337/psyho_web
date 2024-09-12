# Dockerfile для фронтенда

# Используем Node.js образ для сборки фронтенда
FROM node:16-alpine AS build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все файлы и собираем приложение
COPY . .
RUN npm run build

# Используем Nginx для сервировки статических файлов
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Открываем порт для доступа к приложению
EXPOSE 80
