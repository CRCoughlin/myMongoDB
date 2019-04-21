#!/usr/bin/python
import json
from bson import json_util
import datetime
from bottle import route, run, request, abort
from pymongo import MongoClient
import sys


class MyMongoDB:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def connectTo(self, dbName, docName):
        self.db = self.client[dbName]
        self.document = self.db[docName]

        if dbName in self.client.list_database_names():
            print("The database exists.")

    @route('/50day', method='POST')
    def day50(self):
        data = json.load(request.body)
        low = data['low']
        high = data['high']

        pip = [{"$match": {"50-Day Simple Moving Average": {"$gt": low, "$lt": high}}},
               {"$group": {"_id": 1, "count": {"$sum": 1}}}]
        cursor = self.document.aggregate(pip)
        result = list(cursor)
        result = "{'count' : " + str(result[0]["count"]) + "}\n"
        return json.loads(json.dumps(result, indent=4, default=json_util.default))


    @route('/industry', method='GET')
    def industry(self):
        industry = request.query.industry
        pip = [{"$match": {"Industry": industry}}, {"$project": {"_id": 0, "Ticker": 1}}]
        cursor = self.document.aggregate(pip)
        result = list(cursor)
        string = ""
        for tik in result:
            string += str(tik['Ticker']) + ", "
        string = string[:-2]
        result = "{'Tickers': {" + str(string) + "}}\n"
        return json.loads(json.dumps(result, indent=4, default=json_util.default))


    @route('/sectorOutstanding', method='GET')
    def sectorOutstanding(self):
        sector = request.query.sector
        pip = [{"$match": {"Sector": sector}},
               {"$group": {"_id": "null", "Total Shares Outstanding": {"$sum": "$Shares Outstanding"}}},
               {"$project": {"_id": 0, "Total Shares Outstanding": 1}}]
        cursor = self.document.aggregate(pip)
        result = list(cursor)
        result = "{'Total Shares Outstanding' : " + str(result[0]['Total Shares Outstanding']) + "}\n"
        return json.loads(json.dumps(result, indent=4, default=json_util.default))


    @route('/summary', method='GET')
    def stockSummary(self):
        ticker = request.query.ticker
        query = {"Ticker": ticker}
        stock = self.document.find_one(query)
        print(stock)
        result = "{'52-Week High' : " + str(stock["52-Week High"]) + ",\n" \
                                                                     "'52-Week Low' : " + str(stock["52-Week Low"]) + ",\n" \
                                                                                                                      "'Company' : '" + str(
            stock["Company"]) + "',\n" \
                                "'Ticker' : '" + str(stock["Ticker"]) + "',\n" \
                                                                        "'P/E' : " + str(stock["P/E"]) + ",\n" \
                                                                                                         "'Volume' : " + str(
            stock["Volume"]) + ",\n" \
                               "'50-Day Low' : " + str(stock["50-Day Low"]) + ",\n" \
                                                                              "'50-Day High' : " + str(
            stock["50-Day High"]) + ",\n" \
                                    "'Price' : " + str(stock["Price"]) + ",\n" \
                                                                         "'Change' : " + str(stock["Change"]) + "}\n"
        return json.loads(json.dumps(result, indent=4, default=json_util.default))


    @route('/top5', method='GET')
    def top5(self):
        sector = request.query.sector
        query = {"Sector": sector}, {"_id": 0, "Company": 1, "Change": 1}
        sot = {"Change": -1}
        result = self.document.find(query).sort(sot).limit(5)
        return json.loads(json.dumps(result, indent=4, default=json_util.default))




# for database testing
if __name__ == '__main__':
    run(host='localhost', port=8080)


