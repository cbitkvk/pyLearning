import datetime
import pymysql
from PyLearning.Stocks.Stock import *

def build_dates_for_year(year=2018):
    strt_dt = datetime.date(year=year, month=1, day=1)
    dt_list = list()
    dt_list.append(strt_dt.strftime("%Y-%m-%d"))
    for r in range(365):
        strt_dt += datetime.timedelta(days=1)
        if strt_dt.isoweekday() <=5:
            dt_list.append(strt_dt.strftime("%Y-%m-%d"))
    print(dt_list)
    return dt_list

def get_db_connection():
    con = pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return con


def get_next_run_date(con):
    cur = con.cursor()
    rec_cnt = cur.execute("select min(dt) as min_dt From stocks.date_list where loaded is null")
    rec = cur.fetchall()
    print(rec)
    if rec[0]['min_dt'] > datetime.date.today()-datetime.timedelta(days=1):
        return None
    else:
        return rec[0]['min_dt'].strftime("%Y-%m-%d")


if __name__ == "__main__":
    dt_list = build_dates_for_year()
    con = get_db_connection()
    #cur = con.cursor()
    print(dt_list[0])
    #for dt in dt_list:
    #    cur.execute("insert into stocks.date_list(dt) values (%s)", args=dt)
    #con.commit()
    next_dt = get_next_run_date(con)
    print(next_dt)
