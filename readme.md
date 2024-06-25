# Water project

## Overview

For my raspberry pi controlled garden watering system

I'm using the GPIO pins on the raspberry pi to control some relays and pump which water my garden from a rain collection system.

The GPIO uses a level shifter (3.3V to 5V) to control the 5v relays. The 5V also go to the valves. The pump is 120V and is also controlled by a relay.

I collect rain water in IPC totes.

The goal is to schedule the watering of the garden using something like `cron` and also have a web interface to control the watering system.

![Image description](imgs/waterproject.png)

![Image description](imgs/schedule2.png)

## Code

The code is written in python and uses the `fastapi` web framework.

using virtual envirometnt or conda

enviroment is called

`waterproject`

export depedency lsit with pip

```bash
pip freeze > requirements.txt
```

create conda env with

```bash
# conda create --name waterproject --file requirements.txt
 conda create --name waterproject  python=3.11
 pip install -r requirements.txt
```

## Device configuration

You can modify your PINS, location, and name by changing the `devices.json` file. Mine looks like.

```json

[
    {
      "name": "power_cable_solenoid",
      "pin": 12,
      "location": "Top of Water Containers"
    },
    {
      "name": "valve_1",
      "pin": 25,
      "location": "Middle Garden"
    },
    {
      "name": "valve_2",
      "pin": 23,
      "location": "Rock Wall Garden"
    },
    {
      "name": "valve_3",
      "pin": 18,
      "location": "Grape Garden"
    }
  ]
  
```

## start the server as a services

```bash
sudo nano /etc/systemd/system/uvicorn.service
```

Put something like this

```init
[Unit]
Description=Uvicorn App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/git/waterproject
ExecStart=/bin/bash /home/pi/git/waterproject/run_server.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Then

```bash
sudo systemctl daemon-reload
sudo systemctl enable uvicorn.service

# check status with 
sudo systemctl status uvicorn.service
sudo journalctl -u uvicorn.service | tail -n 30

```

I added a static IP on my home network to the raspberry pi so I can access the web interface from any device on my network.


## Future

* edit schedule
* add more devices
* measure the water level 
* add a camera to take pictures of the garden
* pull weather data to adjust watering schedule
* add some unit and integration testing

