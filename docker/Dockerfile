FROM python:3.9.18

WORKDIR /app

# Installiere Abhängigkeiten
RUN apt-get update && apt-get -y install python3-dev libcups2-dev

# Kopiere nur die notwendigen Dateien zuerst, um Docker-Caching zu nutzen
COPY ./pyproject.toml ./poetry.lock /app/
COPY ./config /app/config
COPY ./src /app/src
COPY ./tests /app/tests

# Installiere Poetry und Projekt-Abhängigkeiten
RUN curl -sSL https://install.python-poetry.org | python3.9 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install --without dev

# Setze den Ausführungsbefehl beim Containerstart
CMD ["poetry", "run", "flask", "--app", "src/frontend/flask_app", "run", "--host", "0.0.0.0"]
