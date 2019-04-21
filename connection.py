#!/usr/bin/python
import json
from bson import json_util
import datetime
from bottle import route, run, request, abort
from pymongo import MongoClient
import sys
import mongoDB.myMongoDB


class Connection:

    def __init__(self):
        run(host='localhost', port=8080)
        return None

    @route('/connect', method='GET')
    def connect(self):
        db = request.query.db

    @route('/ping', method='GET')
    def ping(self):
        string = "{Pong: " + request.query.ping + "}\n"
        return json.loads(json.dumps(string, indent=4, default=json_util.default))




