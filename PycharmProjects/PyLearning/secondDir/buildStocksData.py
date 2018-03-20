from PyLearning.Stocks.Stock import *
import logging


def set_header_url():
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q = 0.7,*;q = 0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q = 0.8',
        'Connection': 'keep-alive'}
    return hdr


symbol = "INFY"
start_date = "01-03-2018"
end_date = "20-03-2018"

url = """https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={}&
segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate={}&toDate={}&
dataType=PRICEVOLUMEDELIVERABLE""".format(symbol, start_date, end_date)


def set_logger(logger_object, module_name):
    logger_object.setLevel(logging.INFO)

    log_file = logging.FileHandler(filename="D://pythonLogging//" + module_name + ".log", mode="w")
    log_file.setLevel(logging.INFO)

    stdout = logging.StreamHandler()
    stdout.setLevel(logging.INFO)

    err_file = logging.FileHandler(filename="D://pythonLogging//" + module_name + ".err", mode="w")
    err_file.setLevel(logging.ERROR)

    logger_object.addHandler(log_file)
    logger_object.addHandler(err_file)
    logger_object.addHandler(stdout)


def main(args):
    process_logger = logging.getLogger(__name__)
    mod_name = __file__.__str__().split("/")[-1].replace(".py", "")
    set_logger(process_logger, mod_name)
    p = Stock({"script_name": "INFY"}).download_stock_price()
    print(p)
    if False:
            stock_dict = dict()
            stock_dict['script_name'] = "hello"
            stock_dict['previous_close'] = 100.1
            stock_dict['today_open'] = 101.1
            stock_dict['prev_close'] = 99.1
            stock_dict['open_price'] = 100.1
            stock_dict['high_price'] = 120
            stock_dict['low_price'] = 80
            stock_dict['last_price'] = 97
            stock_dict['close_price'] = 120
            stock_dict['avg_price'] = 190
            stock_dict['ttl_trd_qnty'] = 20000
            stock_dict['turnover_lacs'] = 8000
            stock_dict['no_of_trades'] = 5552131
            stock_dict['deliv_qty'] = 123165
            stock_dict['deliv_per'] = 651
            stck = Stock(stock_dict)
            print(type(stck))
            print(stck.__repr__())
            print(stck)


if __name__ == "__main__":
    main("")


# https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=INFY&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day
# https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=INFY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-03-2018&toDate=20-03-2018&dataType=PRICEVOLUMEDELIVERABLE
