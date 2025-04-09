FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY business_service.py .

EXPOSE 5002

CMD ["uvicorn", "business_service:app", "--host", "0.0.0.0", "--port", "5002"]