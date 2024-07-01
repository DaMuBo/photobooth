# Python Photobooth project
Just a small fun project for me for hustling with flask, python applications and more.
## :rocket:

# Contents
1. [Installation](#installation)
   1. [Install Raspi Dependencies](#install-raspi-dependencies)
   2. [Install Project](#install-project)
   3. [Configure Raspi](#configure-raspi)
2. [Run Service](#run-service)

# Installation
You need to do some configurations to successfully run the project
You will need the most actual raspi os installed. 
At the Moment it's bookworm or bullseye. I used bullseye for this.

## Install Raspi Dependencies
If not already done install libcamera in your raspi.
````commandline
# get latest updates
sudo apt update 
sudo apt upgrade

# install libcamera
sudo apt libcamera-apps
````

You can test the function of your camera with `libcamera-hello`. 
If it's not working it helped to reinstall libcamera with `sudo apt remove libcamera-apps` and after that install it again with `sudo apt install libcamera-apps` 

After this you will need the gstreamer plugin installed. 
-> libcamera is not directly supported by chromium. For running the webcam in the browser we need to stream the video from the actual device to a virtual device

install gstreamer tools with
````commandline
# install a missing dependency
sudo apt-get install libx264-dev libjpeg-dev
# install the remaining plugins
sudo apt-get install libgstreamer1.0-dev \
   libgstreamer-plugins-base1.0-dev \
   libgstreamer-plugins-bad1.0-dev \
   gstreamer1.0-plugins-ugly \
   gstreamer1.0-tools \
   gstreamer1.0-gl \
   gstreamer1.0-gtk3 \
   gstreamer1.0-libcamera
````
install loopback device: `sudo apt install v4l2loopback-dkms`

Your gonna need to install the following dependencies for installing the python project without errors:
1. libcairo2-dev pkg-config python3-dev libgirepository1.0-dev
```
sudo apt install libcairo2-dev pkg-config python3-dev libgirepository1.0-dev
```

## Install Project
For installing the Project on your raspberry you will need to install all requirements
you can use a virtual environment for isolating the packages. But you will probably not use the Raspi  for other stuff. So you can directly install it.
````commandline
pip install -r requirements.txt
````

now you can manually run the service for tests.

## Configure Raspi

Make shure you installed all dependencies from [Install Raspi Dependencies](#install-raspi-dependencies)

Follow these steps for using a GStreamer Pipeline. I linked the source someone already described it. But also the described steps for solving the issue.
https://forums.raspberrypi.com/viewtopic.php?t=351986

1. check your cameras: `libcamera-hello --list-cameras`
2. make it run on boot. go to /etc and open file modules. add v4l2loopback to the file.
````commandline
cd /etc
sudo nano modules
````
3. open /etc/modprobe.d/v4l2loopback.conf and write the options where to write the stream. The default is video_nr=1 In the src/frontend/routes/route_gst_pipes.py the gstreamer pipeline is configured and defaults to video1 if you have multiple cameras you have to change it

```
options v4l2loopback video_nr=1 exclusive_caps=1
```
4. reboot `sudo reboot`
5. check for available device /dev/video1 with `sudo v4l2-ctl --list-devices`

# Run Application
For running the application you can use `flask --app src/frontend/flask_app.py run` for running the application from projects root

setup the service for starting on boot you also can use an own systemd service. Please make shure to correct the paths to your project root for a functioning service !
```
[Unit]
Description=Photobooth Service
After=network.target

[Service]
Environment="XDG_RUNTIME_DIR=/run/user/$(id -u)"
User=pifotoadmin
WorkingDirectory=/home/pifotoadmin/projects/photobooth
Environment="DISPLAY=:0"
ExecStart=/bin/bash -c 'source /home/pifotoadmin/projects/photobooth/.venv/bin/activate && exec flask --app src/frontend/flask_app.py run'
ExecStartPost=/bin/bash -c 'sleep 5 && /usr/bin/chromium-browser --kiosk http://localhost:5000'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

After this add some environment variables via .env file with the following infos:
1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY
3. AWS_DEFAULT_REGION
4. S3_BUCKET_NAME
5. LAYOUT_TEXT
6. PRINTER_NAME

Congratulations your Photobooth Application is up and running !

build from scratch:
# Klone und baue libcamera
RUN git clone https://github.com/raspberrypi/libcamera.git /app/libcamera && \
    cd /app/libcamera && \
    meson setup build --buildtype=release -Dpipelines=rpi/vc4,rpi/pisp -Dipas=rpi/vc4,rpi/pisp -Dv4l2=true -Dgstreamer=enabled -Dtest=false -Dlc-compliance=disabled -Dcam=disabled -Dqcam=disabled -Ddocumentation=disabled -Dpycamera=enabled && \
    ninja -C build install