import os
import telnetlib
import time
import requests
import time
from flask import Flask
from flask_restful import Resource, Api
import argparse

import sys



app = Flask(__name__)
api = Api(app)


_NEWLINE = '\r\n'


BLUEBOLT_IP = os.getenv("HOST")

TELNET_PORT = 23

def run_async(func):
    """
        run_async(func)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object

            E.g.:
            @run_async
            def task1():
                do_something

            @run_async
            def task2():
                do_something_too

            t1 = task1()
            t2 = task2()
            ...
            t1.join()
            t2.join()
    """
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def login():
    connection = False
    session = telnetlib.Telnet(BLUEBOLT_IP, TELNET_PORT)
    print "Successfully Logged in to Panamax"
    return session


def send_command(session, outlet, command):
    session.write('#CYCLE {}:{}\r\n'.format(outlet, command))
    return "OK"


class Command(Resource):
    """
    Generic API resource for interacting with Bluebolt devices.

    Power cycle outlet 1

    #CYCLE 1:5
    /api/cycle/1/5

    Power cycle outlet 2

    #CYCLE 2:5
    /api/cycle/2/5


    """
    # TODO Need to determine if we can get status


    def post(self, outlet, command):
        session = login()
        send_command(session, outlet, command)
        # Need better validation here, for now we assume the command worked
        return "OK"

# Expose Bluebolt commands directly as API
api.add_resource(Command, '/api/<string:outlet>/<string:command>')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)
