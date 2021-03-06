import pandas
import pymysql
import numpy
import datetime
import traceback

def get_connection_details():
    return pymysql.connect(host='localhost', user='root', password='vinay', db='stocks',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def main_pandas():
    conn = get_connection_details()
    df = pandas.read_sql("select * from stocks.script_detailed_info_history "
                         "  order by stock_date desc", conn)
    df_grp = df.groupby('script_name')
    return_list = list()
    for grp, local_df in df_grp:
        try:
            print("processing {}".format(grp))
            local_df['stock_date'] = pandas.to_datetime(local_df['stock_date'], format='%Y-%m-%d')
            local_df.set_index(keys='stock_date', inplace=True)

            mx = local_df['close_price'].max()
            mn = local_df['close_price'].min()
            today_close_price = local_df['close_price'].iloc[0]
            start_of_year_close_price = local_df['close_price'].iloc[-1]
            ytd_change = (today_close_price - start_of_year_close_price) / today_close_price * 100

            weeklymax = local_df['close_price'][0:5].max()
            weeklymin = local_df['close_price'][0:5].min()
            weeklyavg = local_df['close_price'][0:5].mean()

            weekstart = local_df['close_price'][5]
            weekend = local_df['close_price'][0]
            week_change = (weekend - weekstart) / weekend * 100

            year = datetime.date.today().year
            month_id = datetime.date.today().month
            if datetime.date.today().day <= 7:
                month_id -= 1
            if month_id <= 9:
                month_id = '0'+str(month_id)
            else:
                month_id = str(month_id)

            month_max = local_df[str(year) + '-' + month_id]['close_price'].max()
            month_min = local_df[str(year) + '-' + month_id]['close_price'].min()
            month_avg = local_df[str(year) + '-' + month_id]['close_price'].mean()

            month_start = local_df[str(year) + '-' + month_id]['close_price'][-1]
            month_end = local_df[str(year) + '-' + month_id]['close_price'][0]
            mtd_change = (month_end - month_start)/month_end*100

            per_from_this_year_high =  ( today_close_price  - mx)/today_close_price *100


            return_df = dict({"year_min": mn, "year_max": mx, "ytd_change": ytd_change,
                              "weeklymax": weeklymax, "weeklymin": weeklymin, "weeklyavg": weeklyavg,
                              "week_change": week_change,
                              "month_max": month_max, "month_min": month_min, "month_avg": month_avg,
                              "mtd_change": mtd_change, "per_from_this_year_high": per_from_this_year_high})
            return_df['script_name'] = grp
            return_list.append(return_df)
        except Exception as p:
            print("Processing {} failed".format(grp))
            traceback.print_exc()
    summary_report_df = pandas.DataFrame(return_list)
    summary_report_df.set_index(keys='script_name', inplace=True)
    summary_report_df = summary_report_df [['year_max', 'year_min', 'ytd_change',
                                            'month_max', 'month_min', 'month_avg', 'mtd_change',
                                            'weeklymax', 'weeklymin', 'weeklyavg', 'week_change', 'per_from_this_year_high']]
    return summary_report_df


if __name__ == '__main__':
    main_pandas()