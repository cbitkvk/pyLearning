from PyLearning.Stocks.Stock import *
import logging
import ast
import pickle
import pymysql
import threading
import datetime
from queue import Queue

import urllib.request
import urllib.request
import traceback
from PyLearning.Stocks.StockHtmlParser import StockHtmlParser
import pymysql
import logging
from decimal import *

from html.parser import HTMLParser


class StockHtmlParser(HTMLParser):
    def __init__(self, convert_charrefs=True):
         # super(HTMLParser).__init__(convert_charrefs=True)
        self.tr_count = 0
        self.tbody_count = 0
        self.column_count = 0
        self.top_count = 0
        self.stock_dicts = list()
        self.stock_dict = dict()
        self.header_names = list()
        self.rawdata = ""
        self.offset = 0
        self.convert_charrefs = convert_charrefs
        self.cdata_elem = None
        self.lasttag = '???'
        self.interesting = None
        self.lineno = 0

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'table':
            self.top_count += 1
        if tag == "tr":
            if self.tr_count:
                self.stock_dicts.append(self.stock_dict)
            self.tr_count += 1
            # Not the ideal way, but i am resetting the column count to 0
            # so that we can access column/header names while reading data
            self.column_count = 0
        if tag == "tbody":
            self.tbody_count += 1
        if tag in ["td", "th"]:
            self.column_count += 1

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if tag == 'tr':
            self.tr_count += 1

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        try:
            if self.tr_count == 1:
                if "\n\t" not in data and ' ' != data:
                    self.stock_dict[data] = None
                    self.header_names.append(data)
            else:
                if self.column_count <= len(self.header_names):
                    if "\n\t" not in data:
                        self.stock_dict[self.header_names[self.column_count - 1]] = data
                        # print(data)
                        # print(self.header_names[self.column_count-1])
                    # print("column count", self.column_count)
                    # print("header count", len(self.header_names))
                    # self.stock_dict['abc'] =self.column_count
                    # print(self.header_names)
        except Exception as p:
            print(self.tr_count)
            print(self.header_names)
            print(self.column_count)

        # print(self.stock_dict)

    def close(self):
        return self.stock_dict


def set_header_url():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://cssspritegenerator.com',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    return hdr

script_name = "INFY"
hdr = set_header_url()
url = """https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={}&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE""".format(
    script_name)
rqst = urllib.request.Request(url, headers=hdr)
rsp = urllib.request.urlopen(rqst)

data_html = rsp.read().decode("utf-8").replace("<br />", " ")
stock_dict = dict()
prs = StockHtmlParser()
if not ("No Record Found" in data_html or " No Records  " in data_html):
    prs.feed(data_html)
    print(prs.stock_dict)
    print(prs.stock_dicts)

def get_connection_details():
        return pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def convert_decimal( val):
        return None if (val == None or val == "-") else val.replace(",", "")

connection = get_connection_details()
r = connection.cursor()
sql = "insert into stocks.stock_names values(%s, %s, %s)"
print("wrinting to db")
r.execute(sql, args=(1, script_name, "NSE"))
sql2 = "insert into stocks.script_detailed_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
for scp in prs.stock_dicts:
    r.execute(sql2, args=(scp["Symbol"], convert_decimal(scp["Prev Close"]),
                      convert_decimal(scp["Open Price"]),
                      convert_decimal(scp["High Price"]),
                      convert_decimal(scp["Low Price"]),
                      convert_decimal(scp["Last Price"]),
                      convert_decimal(scp["Close Price"]),
                      convert_decimal(scp["VWAP"]),
                      convert_decimal(scp["Total Traded  Quantity"]),
                      convert_decimal(scp["Turnover "]),
                      convert_decimal(scp["No. of  Trades"]),
                      convert_decimal(scp["Deliverable Qty"]),
                      datetime.datetime.strptime(scp["Date"], "%d-%b-%Y").strftime("%Y-%m-%d")))
connection.commit()
