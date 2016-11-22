Bluebolt REST API
=============

This is simple Flask based API for interacting with Panamax Bluebolt


## Installing

After downloading, install using setuptools.

    pip install -r requirements.txt
    python main.py

## Docker


The latest build of this project is also available as a Docker image from Docker Hub

    docker pull kecorbin/bluebolt-api
    sudo docker run -d --restart=always -e HOST=<IP OF BLUEBOLT> --name bluebolt-api --net=host kecorbin/bluebolt-api

## Usage

### Device Command Examples


## Smarthings Integration

**TODO**

