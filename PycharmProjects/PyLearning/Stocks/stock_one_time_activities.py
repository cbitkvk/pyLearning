import datetime
from PyLearning.Stocks.Stock import *


def build_dates_for_year(year=2018):
    strt_dt = datetime.date(year=year, month=1, day=1)
    dt_list_inner = list()
    dt_list_inner.append(strt_dt.strftime("%Y-%m-%d"))
    for r in range(365):
        strt_dt += datetime.timedelta(days=1)
        if strt_dt.isoweekday() <= 5:
            dt_list_inner.append(strt_dt.strftime("%Y-%m-%d"))
    print(dt_list_inner)
    return dt_list_inner


def get_db_connection():
    conn = pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return conn


def get_next_run_date(conn):
    cur = conn.cursor()
    rec_cnt = cur.execute("select min(dt) as min_dt From stocks.date_list where loaded is null")
    print(rec_cnt)
    rec = cur.fetchall()
    print(rec)
    if rec[0]['min_dt'] > datetime.date.today():
        return None
    else:
        return rec[0]['min_dt'].strftime("%Y-%m-%d")


def get_report_data(conn, type):
    curr = conn.cursor()
    if type == 'fluc':
        return_cnt = curr.execute("select * from stocks.script_detailed_info_history where stock_date = %s "
                              "and abs(fluctuation) > 10 order by fluctuation desc", args='2018-04-10')
    elif type == "change" :
        return_cnt = curr.execute("select * from stocks.script_detailed_info_history where stock_date = %s "
                                  "and abs(per_change_today) > 10 order by per_change_today desc", args='2018-04-10')
    elif type == "weeklytrend":
        return_cnt = curr.execute("select * from ( select curr.script_name as script_name, "
                                  "(curr.close_price - hist.open_price)/hist.open_price*100 week_per_change from "
                                  "stocks.script_detailed_info curr "
                                  "inner join stocks.script_detailed_info_history hist "
                                  "on hist.script_name = curr.script_name "
                                  "and hist.stock_date = ( "
                                  "select max(dl.dt) From (select max(dt) as mx from stocks.date_list "
                                  "where loaded = 'Y') cur "
                                  "inner join stocks.date_list dl "
                                  "on datediff(cur.mx,dl.dt)>=7)) a where abs(week_per_change) > 10 order by week_per_change")

    else:
        print("invalid input")
        exit(1)
    data_list = list()
    for i in range(return_cnt):
        rec = curr.fetchone()
        data_list.append(rec.copy())
        if i == 0 :
            col_headers = rec.keys()
            print(col_headers)
        print(rec)
    return data_list


def get_email_credentials():
    fh = open("C:\\Users\\Dell\\Desktop\\stocks.config", 'r')
    config_data = fh.read()
    username = config_data.split("\n")[0].split("=")[1]
    password = config_data.split("\n")[1].split("=")[1]
    return {"user":username, "password":password}


def send_report(email_id, password, conn):
    import smtplib
    import pandas
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # server.login("stocks.reportgen@gmail.com", "Narendramodi")
    email_cred_dict = get_email_credentials()
    server.login(email_cred_dict["user"], email_cred_dict["password"])

    data_list_fluc = get_report_data(conn,"fluc")
    data_list_change = get_report_data(conn,"change")
    data_list_weeklytrend = get_report_data(conn,"weeklytrend")

    registered_user_list_cur = conn.cursor()
    registered_user_list = registered_user_list_cur.execute("select * from stocks.registered_users")

    rec = registered_user_list_cur.fetchone()
    registered_user_list_dict = {}

    while rec:
        try:
            registered_user_list_dict[rec['name']]
            username = rec['name']
            (registered_user_list_dict[username]['emailid']).append(rec['emailid'])
            (registered_user_list_dict[username]['report_type']).append(rec['report_type'])
        except KeyError as p:
            username = rec['name']
            registered_user_list_dict[username] = dict()
            registered_user_list_dict[username]['emailid'] = list()
            (registered_user_list_dict[username]['emailid']).append(rec['emailid'])
            registered_user_list_dict[username]['report_type'] = list()
            (registered_user_list_dict[username]['report_type']).append(rec['report_type'])
        rec = registered_user_list_cur.fetchone()


    df_fluc = pandas.DataFrame(data_list_fluc)
    df_change = pandas.DataFrame(data_list_change)
    df_weeklytrend = pandas.DataFrame(data_list_weeklytrend)

    columns_to_remove_from_report = ['vwap', 'last_price', 'turnover', 'deliverable']
    report_columns_order = ['script_name', 'stock_date', 'close_price', 'low_price', 'high_price',
                            'per_change_today', 'fluctuation', 'no_of',
                            'open_price', 'prev_close',  'ttl_trd']
    df_fluc.drop(axis=1, columns = columns_to_remove_from_report, inplace=True)
    df_change.drop(axis=1, columns = columns_to_remove_from_report, inplace=True)
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
    server.sendmail("Stocks App", "vinaykumarkhambhampati@gmail.com", message.as_string())
    server.sendmail("Stocks App", "manoj.kbti@gmail.com", message.as_string())


if __name__ == "__main__":
    dt_list = build_dates_for_year()
    con = get_db_connection()
    # cur = con.cursor()
    print(dt_list[0])
    # for dt in dt_list:
    #    cur.execute("insert into stocks.date_list(dt) values (%s)", args=dt)
    # con.commit()
    next_dt = get_next_run_date(con)
    print(next_dt)

