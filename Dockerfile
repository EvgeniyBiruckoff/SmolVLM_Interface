FROM python:3.10-slim

WORKDIR /app

ENV DEVICE=cuda
ENV NN_VER=256M

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "main.py"]
