import urllib.request
import traceback
from PyLearning.Stocks.StockHtmlParser import StockHtmlParser


def set_header_url():
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://cssspritegenerator.com',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    return hdr


class Stock:
    def __init__(self, stock_dict):
        self.script_name = stock_dict['script_name']
        self.date_list = stock_dict['date_list'][0]
        self.exchange = stock_dict['exchange']

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
        print("URL:", url)
        rqst = urllib.request.Request(url, headers=hdr)
        rsp = urllib.request.urlopen(rqst)
        # commenting for testing

        # Here we get the response as binary str. we need to convert to utf-8 string.
        # hence using decode
        # data_html would be html file in utf-8 encoding format now.

        data_html = rsp.read().decode("utf-8").replace("<br />", " ")
        # commented for testing.
        # data_html = """<div class="historic-bar" style="width:542px; margin-bottom:5px;">
		#	<span class="download-data-link"><a download target"_blank" style='cursor:pointer'  >Download file in csv format</a></span>
		# </div>
		# <div id='csvContentDiv' style='display:none;'>"Date","Symbol","Series","Open Price","High Price","Low Price","Last Traded Price ","Close Price","Total Traded Quantity","Turnover (in Lakhs)":"21-Mar-2018","INFY","EQ","1,170.00","1,175.50","1,162.20","       1166.20","1,167.50","38,46,497","45,062.71":</div>
	

# <table><tbody><tr><th>Date</th><th>Symbol</th><th>Series</th><th>Open Price</th><th>High Price</th><th>Low Price</th><th>Last Traded Price </th><th>Close Price</th><th>Total Traded Quantity</th><th>Turnover (in Lakhs)</th></tr>
# <tr><td>21-Mar-2018</td><td>INFY</td><td>EQ</td><td>1,170.00</td><td>1,175.50</td><td>1,162.20</td><td>       1166.20</td><td>1,167.50</td><td>38,46,497</td><td>45,062.71</td></tr>
# </tbody></table>
# """
        print("****Full response****")
        print(data_html)
        print("****Full response****")
        # convert data to dict
        stock_dict = dict()
        prs = StockHtmlParser()
        if not "No Record Found" in data_html:
            prs.feed(data_html)
            self.set_class_variables(prs.stock_dict)

    def set_class_variables(self, stock_dict):
        # self.previous_close = stock_dict['previous_close']
        # self.today_open = stock_dict['today_open']
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
        self.deliverable = stock_dict['Deliverable Qty']
        #self.dly_qt_to = stock_dict['% Dly Qt to Traded Qty']



