#!/usr/bin/python
import json
from bson import json_util
import datetime
from bottle import Bottle, route, run, request, abort
from pymongo import MongoClient
import sys
from mongoDB import myMongoDB


class Connection:
    def __init__(self, host, port):
        self.myDB = myMongoDB.MyMongoDB()
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def _route(self):
        self._app.route('/', method="GET", callback=self.hello)
        self._app.route('/ping', callback=self.ping)
        self._app.route('/connDB/<db>/<doc>', callback=self.connDB)

    @route('/')
    def hello(self):
        return 'Connected to MyMongoDB'

    @route('/ping', method='GET')
    def ping(self):
        string = "{Pong: " + request.query.ping + "}\n"
        return json.loads(json.dumps(string, indent=4, default=json_util.default))

    @route('/connDB/<db>/<doc>', method='GET')
    def connDB(self, db, doc):
        string = "Connect to " + db + " -> " + doc + ": " + self.myDB.connectTo(db, doc)
        return json.loads(json.dumps(string, indent=4, default=json_util.default))


    """"@route('/connect', method='GET')
    def connect(self):
        db = request.query.db"""

    '''
    @route('/list', method='GET')
    def connect():
        string = self.myDB.getDocs()
        return json.loads(json.dumps(string, indent=4, default=json_util.default))
    '''


if __name__ == '__main__':
    Connection('localhost', 8080).run()
