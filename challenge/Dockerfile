FROM python:3.12-slim

WORKDIR /app

COPY challenge/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY challenge/app ./app
COPY challenge/artifacts ./artifacts
RUN mkdir -p /data

ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/data/dead_architect.db

EXPOSE 5000

CMD ["python", "app/app.py"]
