FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY database_service.py .

EXPOSE 5003

CMD ["uvicorn", "database_service:app", "--host", "0.0.0.0", "--port", "5003"]