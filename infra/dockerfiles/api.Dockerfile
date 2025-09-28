FROM python:3.11-slim

WORKDIR /app

COPY backend ./backend
COPY worker ./worker
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
