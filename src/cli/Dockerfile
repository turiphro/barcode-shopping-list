FROM python:3.8

WORKDIR /app

COPY ./Pipfile /app/Pipfile

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["./barcode_cli.py"]
