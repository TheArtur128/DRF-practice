FROM python:alpine

WORKDIR /practice
COPY . .

RUN apk add poetry && poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver"]
