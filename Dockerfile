FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr, and from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

# Apply migrations (creates the SQLite DB and seeds the two polls), then
# run the dev server bound to all interfaces so it's reachable from the
# host at http://localhost:8002/
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8002"]
