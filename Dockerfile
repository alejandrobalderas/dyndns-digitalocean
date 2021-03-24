FROM python:3.8-slim

RUN pip3 install pipenv

WORKDIR /app
COPY Pipfile .
RUN pipenv install --skip-lock

COPY main.py .env ./

CMD [ "pipenv", "run", "python", "main.py" ]