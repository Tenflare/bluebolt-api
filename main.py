import os
import telnetlib
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


_NEWLINE = '\r\n'

BLUEBOLT_IP = os.getenv("HOST")
TELNET_PORT = 23
OUTLETS = 8


def login():
    session = telnetlib.Telnet(BLUEBOLT_IP, TELNET_PORT)
    print "Successfully Logged in to Panamax"
    return session


class Switch(Resource):
    """
    # SWITCH 1 ON/OFF

    :param session:
    :param outlet:
    :param state:
    :return:
    """
    def post(self, outlet, state):
        session = login()

        session.write('!SWITCH {} {}\r\n'.format(outlet, str(state).upper()))

        bb = session.expect(["OUTLET[1-9] = O[NF]."], 3)
        try:
            outlet, status = bb[2].strip().split("=")
            print outlet, status
            return {int(outlet[7]): status.strip()}

        except:

            return {"error": "could not parse bluebolt response"}


class OutletStatus(Resource):

    def get(self):
        session = login()
        session.write('?OUTLETSTAT\r\n')

        bb = session.expect(['OUTLET{} = O[NF].'.format(OUTLETS)], 5)
        resp = dict()
        try:
            outlets = bb[2].split('\r\n')
            for outlet in outlets:
                outlet, status = outlet.strip().split('=')
                resp[int(outlet[7])] = status.strip()
            return resp
        except:
            return {"error": "could not parse bluebolt response"}


class Cycle(Resource):
    def post(self, outlet, delay):
        session = login()
        try:
            session.write('#CYCLE {}:{}\r\n'.format(outlet, delay))
            # Need better validation here, for now we assume the command worked
            # as long delays (15+ seconds) would be a valid use case, and we don't
            # want to wait around
            return {outlet: "rebooting"}
        except:
            return {"error": "something went wrong"}

# Expose Bluebolt commands directly as API
api.add_resource(Cycle, '/cycle/<string:outlet>/<string:delay>')
api.add_resource(Switch, '/switch/<string:outlet>/<string:state>')
api.add_resource(OutletStatus, '/outlet/status')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)
