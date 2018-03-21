import urllib.request
import traceback
from PyLearning.Stocks.StockHtmlParser import StockHtmlParser


def set_header_url():
    hdr = {
        'User-Agent': """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) 
        Chrome/23.0.1271.64 Safari/537.11""",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q = 0.7,*;q = 0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q = 0.8',
        'Connection': 'keep-alive'}
    return hdr


class Stock:
    def __init__(self, stock_dict):
        self.script_name = stock_dict['script_name']
        self.date_list = stock_dict['date_list'][0]
        self.exchange = stock_dict['exchange']

        if False:
            self.previous_close = stock_dict['previous_close']
            self.today_open = stock_dict['today_open']
            self.prev_close = stock_dict['prev_close']
            self.open_price = stock_dict['open_price']
            self.high_price = stock_dict['high_price']
            self.low_price = stock_dict['low_price']
            self.last_price = stock_dict['last_price']
            self.close_price = stock_dict['close_price']
            self.avg_price = stock_dict['avg_price']
            self.ttl_trd_qnty = stock_dict['ttl_trd_qnty']
            self.turnover_lacs = stock_dict['turnover_lacs']
            self.no_of_trades = stock_dict['no_of_trades']
            self.deliv_qty = stock_dict['deliv_qty']
            self.deliv_per = stock_dict['deliv_per']

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

        url = """https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol={}&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day""".format(self.script_name)
        print("URL:", url)
        rqst = urllib.request.Request(url, headers=hdr)
        rsp = urllib.request.urlopen(rqst)
        # Here we get the response as binary str. we need to convert to utf-8 string.
        # hence using decode
        # data_html would be html file in utf-8 encoding format now.
        data_html = rsp.read().decode("utf-8")
        print("****Full response****")
        print(data_html)
        print("****Full response****")
        # convert data to dict
        stock_dict = dict()
        prs = StockHtmlParser()
        prs.feed(data_html)
        self.set_class_variables(prs.stock_dict)

    def set_class_variables(self, stock_dict):
        self.previous_close = stock_dict['previous_close']
        self.today_open = stock_dict['today_open']
        self.prev_close = stock_dict['prev_close']
        self.open_price = stock_dict['open_price']
        self.high_price = stock_dict['high_price']
        self.low_price = stock_dict['low_price']
        self.last_price = stock_dict['last_price']
        self.close_price = stock_dict['close_price']
        self.avg_price = stock_dict['avg_price']
        self.ttl_trd_qnty = stock_dict['ttl_trd_qnty']
        self.turnover_lacs = stock_dict['turnover_lacs']
        self.no_of_trades = stock_dict['no_of_trades']
        self.deliv_qty = stock_dict['deliv_qty']
        self.deliv_per = stock_dict['deliv_per']
