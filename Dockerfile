FROM python:3.12

WORKDIR /app

COPY backend backend

RUN pip install --no-cache-dir -r backend/requirements.txt

COPY frontend frontend

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
