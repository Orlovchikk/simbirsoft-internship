FROM python:3.12-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

WORKDIR /app

CMD ["poetry", "run", "python3", "main.py"] 