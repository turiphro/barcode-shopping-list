FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x ./gunicorn_starter.sh

EXPOSE 5000
ENV PORT=5000
ENV PYTHONUNBUFFERED=TRUE

ENTRYPOINT ["./gunicorn_starter.sh"]
