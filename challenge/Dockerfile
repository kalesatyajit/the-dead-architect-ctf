FROM python:3.12-slim AS builder

WORKDIR /build
RUN apt-get update \
	&& apt-get install -y --no-install-recommends gcc git libc6-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY organizer ./organizer
COPY challenge ./challenge
RUN python organizer/generate_artifacts.py

FROM python:3.12-slim

WORKDIR /app

COPY challenge/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY challenge/app ./app
COPY --from=builder /build/artifacts ./artifacts
RUN mkdir -p /data

ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/data/dead_architect.db

EXPOSE 5000

CMD ["python", "app/app.py"]
