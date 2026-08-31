# Используем официальный образ Nginx
FROM nginx:latest

# создаем директорию для статических файлов
RUN mkdir -p /app/staticfiles

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем порт 80 для HTTP-трафика
EXPOSE 80