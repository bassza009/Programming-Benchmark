FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir psutil
COPY . .
CMD ["python3", "doorNoprint.py"]
