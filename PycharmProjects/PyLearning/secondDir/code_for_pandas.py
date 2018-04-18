import pandas
import pymysql
import numpy

def get_connection_details():
    return pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def main():
    conn = get_connection_details()
    df = pandas.read_sql("select * from stocks.script_detailed_info_history where script_name in ('INFY','DLF') order by stock_date desc", conn)
    df_grp = df.groupby('script_name')
    return_list = list()
    for grp, local_df in df_grp:
        return_df = local_df['open_price'].agg(pandas_agg_method)
        return_df['script_name'] = grp
        print(return_df)
        return_list.append(return_df)
    print(return_list)


def pandas_agg_method(df: pandas.Series) -> dict:
    mx = df.max()
    mn = df.min()
    weeklymax = df[0:5].max()
    weeklymin = df[0:5].min()
    return {"mn": mn, "mx": mx, "weeklymax": weeklymax, "weeklymin": weeklymin}


if __name__ == '__main__':
    main()