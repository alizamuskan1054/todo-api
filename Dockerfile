# Step 1: Base image -> Python already installed hai isme
FROM python:3.12-slim

# Step 2: Container ke andar working directory set karo
WORKDIR /app

# Step 3: Pehle sirf requirements copy karo (Docker layer caching ke liye,
# taake code change hone par dependencies dobara install na ho)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Ab baaki sara project code copy karo
COPY . .
RUN python manage.py collectstatic --noinput
# Step 5: Django ka default port
EXPOSE 8000

# Step 6: Migrations run karke server start karo
CMD ["sh", "-c", "python manage.py migrate && gunicorn todo_api.wsgi:application --bind 0.0.0.0:8000"]
