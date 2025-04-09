FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client_service.py .

EXPOSE 5000

CMD ["uvicorn", "client_service:app", "--host", "0.0.0.0", "--port", "5000"]