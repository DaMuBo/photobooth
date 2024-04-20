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
3. open /etc/modprobe.d/v4l2loopback.conf and write the options where to write the stream.
```
options v4l2loopback video_nr=1 exclusive_caps=1
```
4. reboot `sudo reboot`
5. check for available device /dev/video1 with `sudo v4l2-ctl --list-devices`
6. install a service for automatically run it in the background. for example use systemd unit. For example name it "/etc/systemd/system/gst-pipeline.service"
````commandline
[Unit]
Description=gst-pipeline service
Before=lightdm.service    # adjust accordingly

[Service]
# Ensure the loopback device has been created by the v4l2loopback
# driver before starting the pipeline.
ExecStartPre=sh -c 'while ! test -c /dev/video1; do sleep 0.1; done'
ExecStart=gst-launch-1.0 -vvv \
 libcamerasrc ! \
 capsfilter caps=video/x-raw,width=2304,height=1296,format=NV12 ! \
 v4l2convert ! \
 queue ! \
 v4l2sink device=/dev/video1
 v4l2sink device=/dev/video1
Restart=always

[Install]
RequiredBy=lightdm.service      # adjust accordingly
````
7. start and check the status of your service
````commandline
sudo systemctl daemon-reload
sudo systemctl start gst-pipeline.service
sudo systemctl status gst-pipeline.service

# if needed stop your service
sudo systemctl stop gst-pipeline.service
````
# Run Service
