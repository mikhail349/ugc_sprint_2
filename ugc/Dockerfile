FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

RUN mkdir /app/logs

RUN groupadd -r app \
    && useradd -d /app -r -g app app

COPY --chown=app:app . .

EXPOSE 8000

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "4", "--bind", "0.0.0.0:8000", "src.app.patched:app"]