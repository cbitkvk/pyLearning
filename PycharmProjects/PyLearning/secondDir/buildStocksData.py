import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Stocks'))

from PyLearning.Stocks.Stock import *

def main(args):
    stock_dict = {}
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
