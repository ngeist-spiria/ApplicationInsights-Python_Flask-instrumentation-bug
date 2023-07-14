FROM python:3.11

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

# run flask
CMD python app.py
