FROM arm64v8/python:3.11-bookworm
# FROM debian:bookworm

WORKDIR /app

# Installiere grundlegende Abhängigkeiten
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y software-properties-common curl gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Füge das Raspberry Pi Repository hinzu
RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" | tee /etc/apt/sources.list.d/raspi.list && \
    curl -fsSL https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - && \
    apt update
RUN apt install -y libraspberrypi-bin python3-dev libcups2-dev git build-essential kmod libcamera-apps libcamera-v4l2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Installiere spezifische Abhängigkeiten für libcamera
RUN apt-get update && apt-get install -y \
    libboost-dev \
    libgnutls28-dev openssl libtiff-dev pybind11-dev \
    qtbase5-dev libqt5core5a libqt5widgets5 \
    meson cmake \
    python3-yaml python3-ply python3-jinja2 libcairo2-dev libgirepository1.0-dev v4l-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install jinja2 ply pyyaml


# install libgstreamer dependencies
RUN apt update && apt install -y libgstreamer1.0-dev \
libgstreamer-plugins-base1.0-dev \
libgstreamer-plugins-bad1.0-dev \
gstreamer1.0-plugins-ugly \
gstreamer1.0-tools \
gstreamer1.0-gl \
gstreamer1.0-gtk3 \
gstreamer1.0-libcamera \
gstreamer1.0-plugins-bad

# Installiere v4l2loopback
RUN apt-get update && apt-get install -y v4l2loopback-dkms

# Kopiere nur die notwendigen Dateien zuerst, um Docker-Caching zu nutzen
COPY ./pyproject.toml ./poetry.lock /app/
COPY ./config /app/config
COPY ./samples /app/samples
COPY ./src /app/src
COPY ./tests /app/tests

# Installiere Poetry
# Manuelle Installation von Poetry
RUN pip install poetry

# Installiere Projekt-Abhängigkeiten
RUN poetry config virtualenvs.create false && \
    poetry install --only main,prod

# Füge Skript hinzu, um v4l2loopback zu laden und ein virtuelles Video-Gerät zu erzeugen
COPY ./setup_v4l2loopback.sh /usr/local/bin/setup_v4l2loopback.sh
RUN chmod +x /usr/local/bin/setup_v4l2loopback.sh

# Setze den Ausführungsbefehl beim Containerstart
CMD ["/bin/bash", "-c", "/usr/local/bin/setup_v4l2loopback.sh && poetry run app"]
