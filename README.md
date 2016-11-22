Bluebolt REST API
=============

This is simple Flask based API for interacting with Panamax Bluebolt


## Installing

After downloading, install using setuptools.

    pip install -r requirements.txt
    python main.py

## Docker


The latest build of this project is also available as a Docker image from Docker Hub

    docker build -t bluebolt-api .
    docker run -d --restart=always -e HOST=<IP OF BLUEBOLT> --name bluebolt-api --net=host bluebolt-api

## Usage

### Device Command Examples

```
    Generic API resource for interacting with Bluebolt devices.

    Power cycle outlet 1

    #CYCLE 1:5
    /api/cycle/1/5

    Power cycle outlet 2

    #CYCLE 2:5
    curl -X POST 127.0.0.1/api/cycle/2/5


```
## Smarthings Integration

**TODO**

