FROM python:3.7

WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x ./gunicorn_starter.sh

EXPOSE 5000

ENTRYPOINT ["./gunicorn_starter.sh"]