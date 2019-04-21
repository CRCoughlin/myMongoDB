#!/usr/bin/python
import json
from bson import json_util
import datetime
from bottle import route, run, request, abort
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['market']
collection = db['stocks']

@route('/create', method='POST')
def mongo_create():
    try:
        try:
            data = request.json
        except:
            raise ValueError
        string = collection.insert_one(data)

        if collection.find(data).count() > 0:
            result = "Created\n"
        else:
            result = "Not Created\n"

    except NameError:
        abort(404, "Not Created")

    return json.loads(json.dumps(result, indent=4, default=json_util.default))


@route('/read', method='GET')
def mongo_read():
    try:
        print("READING")
        company = request.query.company
        print(company)
    except:
        raise ValueError
    if company is None:
        raise ValueError

    query = {"Company": company}
    print("Try Find")
    found = collection.find_one(query)
    if found is None:
        found = "Not Found\n"
    return json.loads(json.dumps(found, indent=4, default=json_util.default))


@route('/update')
def mongo_update():
    try:
        try:
            tik = request.query.Ticker
            vol = request.query.Volume
            print("Got input")
            print("Ticker: " + tik)
            print("Volume: " + vol)
        except:
            raise ValueError
        if tik is None or (vol is None and vol > 0):
            raise ValueError

        print("Set Vol")
        search = {"Ticker": tik}
        newData = {"$set": {"Volume": vol}}
        string = collection.update_many(search, newData)
        found = collection.find_one(search)

    except NameError:
        abort(404, "Not Found")
    return json.loads(json.dumps(found, indent=4, default=json_util.default))


@route('/delete', method='GET')
def mongo_delete():
    try:
        try:
            tik = request.query.Ticker
        except:
            raise ValueError
        if tik is None:
            raise ValueError

        query = {"Ticker": tik}
        string = collection.delete_many(query)
        if not collection.find_one(query):
            result = "Deleted\n"
        else:
            result = "Fail\n"

    except NameError:
        abort(404, "Not Found")
    return json.loads(json.dumps(result, indent=4, default=json_util.default))
