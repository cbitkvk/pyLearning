from PyLearning.Stocks.Stock import *
import logging
import ast
import pickle
import pymysql
import threading
import datetime
from queue import Queue


download_parallelism = 4
db_parallelism = 2


def set_header_url():
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q = 0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q = 0.7,*;q = 0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q = 0.8',
        'Connection': 'keep-alive'}
    return hdr


def set_logger(logger_object, module_name):
    logger_object.setLevel(logging.INFO)
    formatter = logging.Formatter("[ %(threadName)s %(asctime)s %(levelname)s ] %(msg)s")

    log_file = logging.FileHandler(filename="D://pythonLogging//" + module_name + ".log", mode="w")
    log_file.setLevel(logging.INFO)
    log_file.setFormatter(formatter)

    stdout = logging.StreamHandler()
    stdout.setLevel(logging.INFO)
    stdout.setFormatter(formatter)

    err_file = logging.FileHandler(filename="D://pythonLogging//" + module_name + ".err", mode="w")
    err_file.setLevel(logging.ERROR)
    err_file.setFormatter(formatter)

    logger_object.addHandler(log_file)
    logger_object.addHandler(err_file)
    logger_object.addHandler(stdout)
    return logger_object


def tables_cleanup():
    con = pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    p = con.cursor()
    sql = "delete from stocks.script_detailed_info"
    sql2 = "delete from stocks.stock_names"
    p.execute(sql)
    p.execute(sql2)
    con.commit()


def mythread_call(stock, sem, con):
    sem.acquire()
    stock.download_stock_price()
    sem.release()
    stock.write_to_db()


def main():
    process_logger = logging.getLogger(__name__)
    mod_name = __file__.__str__().split("/")[-1].replace(".py", "")
    set_logger(process_logger, mod_name)
    process_logger.info(msg="Started db cleanup")
    tables_cleanup()
    process_logger.info(msg="ended db cleanup")
    # p = Stock({"script_name": "INFY", "date_list": ["212"] , "exchange": "NSE"}).download_stock_price()

    # Read the file containing list of stocks on NSE.
    list_of_stocks_str = open("C:\\Users\\Dell\\Desktop\\stock_list_nse.txt").read()
    con = pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    list_of_stocks = ast.literal_eval(list_of_stocks_str)
    date_list = (datetime.date.today()).strftime("%Y-%m-%d")
    exchange = "NSE"
    stocks_dict = {}
    curr_threads = list()

    # added the logic for semaphore. here we want to restict the number of
    # parallel threads to download_parallelism which is 4 here.

    sem = threading.BoundedSemaphore(value=download_parallelism)

    cur_queue = Queue()

    for stk in list_of_stocks:
        p = Stock({"script_name": stk, "date_list": date_list, "exchange": exchange}, process_logger)
    #    th = threading.Thread(target=p.download_stock_price())
    #    th = threading.Thread(target=mythread_call, args=(p, sem, con, ))
    #    th.start()
        p.download_stock_price()
        p.write_to_db()
        stocks_dict[stk] = p
    #    curr_threads.append(th)

    # for tr in curr_threads:
        # tr.join()

    # con.commit()

    for stk, dct in stocks_dict.items():
        print(stk, "->", dct)

    pickle.dump(list_of_stocks, file=open("D://marketdata//todayJson.pkl", 'wb'))


if __name__ == "__main__":
    main()

# https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=INFY&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day
# https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=INFY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-03-2018&toDate=20-03-2018&dataType=PRICEVOLUMEDELIVERABLE
