FROM python:3.10-slim-bullseye as base

ENV PYTHONUNBUFFERED 1

ARG HOMEDIR=/home/app


RUN apt-get update  \
    && apt-get install --no-install-recommends -y \
        git \
        libffi-dev \
        python3-all-dev \
        python3-venv \
        build-essential \
        libpcre3-dev \
        libpq-dev \
        curl \
        libcurl4-openssl-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN chmod +x docker/start.sh

RUN useradd -m -d ${HOMEDIR} -N -G users -u 1313 app
RUN chown -R app:users "/usr/src/app"
USER app

ENTRYPOINT ["uvicorn", "--factory", "app.asgi:build_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]