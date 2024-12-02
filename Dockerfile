FROM python:3.12-alpine

WORKDIR /flask_jwt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "main:app", "--config", "gunicorn.py"]