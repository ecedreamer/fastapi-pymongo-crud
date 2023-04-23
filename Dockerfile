FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
COPY . /app
RUN apk add --no-cache build-base libffi-dev
RUN apk add --no-cache gcc musl-dev
RUN pip install --no-cache-dir -r requirements.txt
#CMD ["python", "server.py"]
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]