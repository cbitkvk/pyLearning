from PyLearning.Stocks.Stock import *
import logging
import ast
import pickle
import pymysql
import threading
import datetime
from queue import Queue

process_logger = None


download_parallelism = 4
db_parallelism = 2


def get_email_credentials():
    fh = open("C:\\Users\\Dell\\Desktop\\stocks.config", 'r')
    config_data = fh.read()
    username = config_data.split("\n")[0].split("=")[1]
    password = config_data.split("\n")[1].split("=")[1]
    return {"user": username, "password": password}


def set_header_url():
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
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


def copy_data_to_history():
    con = pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    sql = 'insert into stocks.script_detailed_info_history ' \
          'select *,(close_price-prev_close)*100/prev_close ' \
          'as per_change_today, (high_price - low_price)*100/low_price ' \
          'as fluctuation from script_detailed_info'
    cur.execute(sql)
    con.commit()


def mythread_call(stock, sem, con):
    sem.acquire()
    stock.download_stock_price()
    sem.release()
    stock.write_to_db()
    print(con)


def get_next_run_date(con):
    global process_logger
    cur = con.cursor()
    rec_cnt = cur.execute("select min(dt) as min_dt From stocks.date_list where loaded is null")
    process_logger.info(msg="rec_cnt from date_list for next run is {}".format(rec_cnt))
    rec = cur.fetchall()
    print(rec)
    if rec[0]['min_dt'] > datetime.date.today():
        return None
    else:
        return rec[0]['min_dt'].strftime("%Y-%m-%d")


def close_this_run(dt, con):
    upd_date_list_cursor = con.cursor()
    upd_date_list_cursor.execute("update stocks.date_list set loaded='Y' where dt = %s", args=dt)
    con.commit()


def get_report_data(conn, report_type, stocks_db_sql_info_dict, date):
    curr = conn.cursor()
    return_cnt = 0
    if report_type == 'fluc':
        return_cnt = curr.execute(stocks_db_sql_info_dict['fluc'], args=date)
    elif report_type == "change":
        return_cnt = curr.execute(stocks_db_sql_info_dict['change'], args=date)
    elif report_type == "weeklytrend":
        return_cnt = curr.execute(stocks_db_sql_info_dict['weeklytrend'])

    else:
        print("invalid input")
        exit(1)
    data_list = list()
    for i in range(return_cnt):
        rec = curr.fetchone()
        data_list.append(rec.copy())
        if i == 0:
            col_headers = rec.keys()
            print(col_headers)
        print(rec)
    return data_list


def send_report(email_id, password, conn, stock_db_sql_info_dict, date):
    user_cred = get_email_credentials()
    print(email_id, password)
    import smtplib
    import pandas
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user_cred['user'], user_cred['password'])
    data_list_fluc = get_report_data(conn, "fluc", stock_db_sql_info_dict, date)
    data_list_change = get_report_data(conn, "change", stock_db_sql_info_dict, date)
    data_list_weeklytrend = get_report_data(conn, "weeklytrend", stock_db_sql_info_dict, date)

    df_fluc = pandas.DataFrame(data_list_fluc)
    df_change = pandas.DataFrame(data_list_change)
    df_weeklytrend = pandas.DataFrame(data_list_weeklytrend)

    columns_to_remove_from_report = ['vwap', 'last_price', 'turnover', 'deliverable']
    report_columns_order = ['script_name', 'stock_date', 'close_price', 'low_price', 'high_price',
                            'per_change_today', 'fluctuation', 'no_of',
                            'open_price', 'prev_close',  'ttl_trd']
    df_fluc.drop(axis=1, columns=columns_to_remove_from_report, inplace=True)
    df_change.drop(axis=1, columns=columns_to_remove_from_report, inplace=True)
    df_fluc = df_fluc[report_columns_order]
    df_change = df_change[report_columns_order]

    # df.to_html()
    msg = df_fluc.to_html()  # The /n separates the message from the headers
    msg2 = df_change.to_html()  # The /n separates the message from the headers
    msg3 = df_weeklytrend.to_html()  # The /n separates the message from the headers

    msg = "<html><h2>Change over and above 10% \n\n</h2>" \
          "::\n\n" + msg2 + "\n <h2>Fluctuation over and above than 10% </h2>\n\n" \
          + msg + "\n <h2>Weekly trend: Change over and above than 10% </h2> \n" + msg3 + "</html>"
    print(msg)
    message = MIMEMultipart(
        "alternative", None, [MIMEText(msg, 'html')])

    server.sendmail("Stocks App", "vinaykumarcbit@yahoo.co.in", message.as_string())
    # server.sendmail("Stocks App", "vinaykumarkhambhampati@gmail.com", message.as_string())
    # server.sendmail("Stocks App", "manoj.kbti@gmail.com", message.as_string())


def main():
    global process_logger
    stock_db_sql_info_dict = stocks_db_sql_info()
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
    # date_list = (datetime.date.today()).strftime("%Y-%m-%d")
    next_dt = get_next_run_date(con)
    if not next_dt:
        print("No dates to process")
        exit(1)
    exchange = "NSE"
    stocks_dict = {}
    curr_threads = list()
    print(curr_threads)

    # added the logic for semaphore. here we want to restict the number of
    # parallel threads to download_parallelism which is 4 here.

    sem = threading.BoundedSemaphore(value=download_parallelism)
    print("{} is not being used".format(sem))

    cur_queue = Queue()
    print("{} is not being used".format(cur_queue))

    for stk in list_of_stocks:
        p = Stock({"script_name": stk, "date_list": next_dt, "exchange": exchange}, process_logger)
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
    copy_data_to_history()
    close_this_run(next_dt, con)
    send_report("a", "b", con, stock_db_sql_info_dict, next_dt)


if __name__ == "__main__":
    main()

# https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/getHistoricalData.jsp?symbol=INFY&series=EQ&fromDate=undefined&toDate=undefined&datePeriod=1day
# https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=INFY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-03-2018&toDate=20-03-2018&dataType=PRICEVOLUMEDELIVERABLE
