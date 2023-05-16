FROM python:3.11-buster

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn  src.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --timeout 0

EXPOSE 8000