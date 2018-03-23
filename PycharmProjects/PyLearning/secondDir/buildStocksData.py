from PyLearning.Stocks.Stock import *
import logging
import ast

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
    # p = Stock({"script_name": "INFY", "date_list": ["212"] , "exchange": "NSE"}).download_stock_price()
    # print(p)

    # Read the file containing list of stocks on NSE.
    list_of_stocks_str = open("C:\\Users\\Dell\\Desktop\\stock_list_nse.txt").read()
    list_of_stocks = ast.literal_eval(list_of_stocks_str)
    stocks_dict = {}
    for stk in list_of_stocks:
        p = Stock({"script_name": stk, "date_list": ["212"], "exchange": "NSE"})
        p.download_stock_price()
        print(p)
        stocks_dict[stk] = p

    for stk, dct in stocks_dict.items():
        print(stk, "->", dct)

if __name__ == "__main__":
    main("")

# https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=INFY&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day
# https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=INFY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-03-2018&toDate=20-03-2018&dataType=PRICEVOLUMEDELIVERABLE
