FROM python:3.12

LABEL maintainer="reginaldo-castro"
LABEL version="1.0"
LABEL description="gerenciador de empréstimos"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    python3-dev \
    curl \
    build-essential \
    postgresql-client \
    netcat-openbsd \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/infra/run.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/infra/run.sh"]