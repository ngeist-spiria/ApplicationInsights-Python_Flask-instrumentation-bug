FROM python:3.11

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

# collect static files
RUN python3 manage.py collectstatic --noinput

# run gunicorn
CMD python manage.py runserver 0.0.0.0:8000
