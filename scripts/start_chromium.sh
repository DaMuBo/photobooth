#!/bin/bash
sleep 5

cd /home/pifotoadmin/projects/photobooth && /home/pifotoadmin/.local/bin/poetry run app &

sleep 3

export DISPLAY=:0.0
su -c "/usr/bin/chromium-browser --kiosk http://localhost:5000" pifotoadmin