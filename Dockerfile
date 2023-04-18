FROM python:alpine
WORKDIR .
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "server.py"]