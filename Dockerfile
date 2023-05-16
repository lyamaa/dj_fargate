FROM python:3.11-buster

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn src.asgi:application -w 2 -k uvicorn.workers.UvicornWorker --log-file - --bind 0.0.0.0:8000

EXPOSE 8000