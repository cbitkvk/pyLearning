import urllib.request
import urllib.request
import traceback
from PyLearning.Stocks.StockHtmlParser import StockHtmlParser
import pymysql
import logging
from decimal import *


def set_header_url():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://cssspritegenerator.com',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    return hdr


class Stock:
    def __init__(self, stock_dict, logg):
        self.mylogger = logg

        self.script_name = stock_dict['script_name']
        self.date_list = stock_dict['date_list']
        self.exchange = stock_dict['exchange']
        self.stock_dict = stock_dict

        # just for temporary to get rid of that warning.
        self.prev_close = None
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.last_price = None
        self.close_price = None
        self.vwap = None
        self.ttl_trd = None
        self.turnover = None
        self.no_of = None
        self.deliverable = None

    def get_price_variation(self):
        try:
            return (self.high_price - self.low_price)/self.high_price
        except ZeroDivisionError or ArithmeticError:
            return "NA"

    def percentage_change(self):
        try:
            return ((self.close_price - self.prev_close)/self.prev_close)*100
        except ZeroDivisionError or ArithmeticError:
            return "NA"

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__

    def download_stock_price(self):
        hdr = set_header_url()
        # url = """https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={}&
        # segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate={}&toDate={}&
        # dataType=PRICEVOLUMEDELIVERABLE""".format(self.script_name, start_date, end_date)

        # url = """https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol={}&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day""".format(self.script_name)
        url = """https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={}&segmentLink=3&symbolCount=1&series=ALL&dateRange=day&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE""".format(self.script_name)
        self.mylogger.info(msg="Started the download of {}".format(self.script_name))
        rqst = urllib.request.Request(url, headers=hdr)
        rsp = urllib.request.urlopen(rqst)

        # Here we get the response as binary str. we need to convert to utf-8 string.
        # hence using decode
        # data_html would be html file in utf-8 encoding format now.

        data_html = rsp.read().decode("utf-8").replace("<br />", " ")
        # print("****Full response****")
        # print(data_html)
        # print("****Full response****")
        # convert data to dict
        stock_dict = dict()
        prs = StockHtmlParser()
        if not ("No Record Found" in data_html or " No Records  " in data_html):
            prs.feed(data_html)
            self.set_class_variables(prs.stock_dict)
            self.mylogger.info(msg="End of download of {}".format(self.script_name))


    def set_class_variables(self, stock_dict):
        self.prev_close = stock_dict['Prev Close']
        self.open_price = stock_dict['Open Price']
        self.high_price = stock_dict['High Price']
        self.low_price = stock_dict['Low Price']
        self.last_price = stock_dict['Last Price']
        self.close_price = stock_dict['Close Price']
        self.vwap = stock_dict['VWAP']
        self.ttl_trd = stock_dict['Total Traded  Quantity']
        self.turnover = stock_dict['Turnover ']
        self.no_of = stock_dict['No. of  Trades']
        self.deliverable = stock_dict['Deliverable Qty'] if stock_dict['Deliverable Qty'] != "-" else None
        # self.dly_qt_to = stock_dict['% Dly Qt to Traded Qty']
        for k,v in stock_dict.items():
            self.stock_dict[k] = v

    def get_connection_details(self):
        return pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def write_to_db(self, connection=None):
        # try:
        #    r = connection.cursor()
        #    print("using input connection")
        # except NameError as exp:
        #   connection = self.get_connection_details()
        #    print("getting connection")
        #    r = connection.cursor()

        connection = self.get_connection_details()
        r = connection.cursor()
        sql = "insert into stocks.stock_names values(%s, %s, %s)"
        print("wrinting to db")
        r.execute(sql, args=(1, self.script_name, self.exchange))
        sql2 = "insert into stocks.script_detailed_info values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # r.execute(sql2, args=(self.script_name, Decimal(self.prev_close.replace(",","")), Decimal(self.open_price.replace(",","")), Decimal(self.high_price.replace(",","")), Decimal(self.low_price.replace(",","")), Decimal(self.last_price.replace(",","")), Decimal(self.close_price.replace(",","")), Decimal(self.vwap.replace(",","")), Decimal(self.ttl_trd.replace(",","")), Decimal(self.turnover.replace(",","")), Decimal(self.no_of.replace(",","")), Decimal(self.deliverable.replace(",",""))))
        r.execute(sql2, args=(self.script_name, self.convert_decimal(self.prev_close),
                              self.convert_decimal(self.open_price),
                              self.convert_decimal(self.high_price),
                              self.convert_decimal(self.low_price),
                              self.convert_decimal(self.last_price),
                              self.convert_decimal(self.close_price),
                              self.convert_decimal(self.vwap),
                              self.convert_decimal(self.ttl_trd),
                              self.convert_decimal(self.turnover),
                              self.convert_decimal(self.no_of),
                              self.convert_decimal(self.deliverable),
                              self.date_list ))
        connection.commit()

    def convert_decimal(self, val):
        return None if (val == None or val == "-") else val.replace(",", "")