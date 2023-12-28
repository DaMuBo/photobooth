FROM python:3.9.18

WORKDIR /app

# Installiere Abhängigkeiten
RUN apt-get update && apt-get -y install gcc python3-dev libcups2-dev

# Kopiere nur die notwendigen Dateien zuerst, um Docker-Caching zu nutzen
COPY ./pyproject.toml ./poetry.lock /app/
COPY ./config /app/config
COPY ./samples /app/samples
COPY ./src /app/src
COPY ./tests /app/tests

# Installiere Poetry und Projekt-Abhängigkeiten
# RUN curl -sSL https://install.python-poetry.org | python3.9 -
# ENV PATH="/root/.local/bin:$PATH"
# RUN poetry install --with prod


# Setze den Ausführungsbefehl beim Containerstart
RUN pip3 install pycups
CMD ["python3", "src/cup_test.py"]

# CMD ["poetry", "run", "flask", "--app", "src/frontend/flask_test", "run", "--host", "0.0.0.0"]
