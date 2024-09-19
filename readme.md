# Сокращатель ссылок

Очень простой сокращатель ссылок

Позволяет создавать сокращенные ссылки и сохранять в базу данных переходы по ним

## Запуск

1. Настраиваем переменное окружение в файле `.env`

   ```dotenv
   BASE_URL=https://example.com
   DB_URL=postgresql+asyncpg://user:password@host:port/db_name
   ```
   
   Или можно использовать настройки по умолчанию, которые эквивалентны

   ```dotenv
   BASE_URL=
   DB_URL=sqlite+aiosqlite:///db.sqlite3
   ```

2. Настраиваем `BASE_URL` в `configs.py`. Это будет путь до сокращенных ссылок

3. Создаем виртуальное окружение python

   Для Windows:

   ```shell
   python -m venv venv
   venv\Scripts\activate
   ```

   Для Linux:

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```

4. Устанавливаем зависимости

   ```shell
   pip install -r requirements.txt
   ```

5. Применяем миграции `alembic upgrade head`

6. [Устанавливаем pm2](https://pm2.keymetrics.io/)

7. `pm2 start main.py --interpreter=venv/bin/python`

## Настройка nginx

### Получение сертификата от [Let's Encrypt](https://letsencrypt.org/)

Прописываем сервер

```nginx configuration
server {
  access_log /var/log/nginx/url-shortener-access.log;
  error_log /var/log/nginx/url-shortener-errors.log;

  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

  server_name example.com;
  set $upstream_backend_url_shortener http://127.0.0.1:8090;

  location ~ ^/(click|generate) {
    proxy_pass          $upstream_backend_url_shortener;
    proxy_set_header    Host $host;
    proxy_set_header    X-Real-IP $remote_addr;
    proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header    X-Forwarded-Proto $scheme;
  }
}
```