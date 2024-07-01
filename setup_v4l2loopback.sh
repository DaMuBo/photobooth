#!/bin/bash

# Lade v4l2loopback Modul
modprobe v4l2loopback devices=1 video_nr=1 card_label="Virtual Cam" exclusive_caps=1

# Überprüfe den Rückgabewert von modprobe
if [ $? -eq 0 ]; then
    echo "v4l2loopback erfolgreich geladen"
else
    echo "Fehler beim Laden von v4l2loopback"
    exit 1
fi

# Überprüfe, ob das Gerät erstellt wurde
if [ -e /dev/video1 ]; then
    echo "Virtuelles Gerät /dev/video1 gefunden"
else
    echo "Virtuelles Gerät /dev/video1 nicht gefunden"
    exit 1
fi

# Starte den Flask-Server oder eine andere Anwendung
exec "$@"
