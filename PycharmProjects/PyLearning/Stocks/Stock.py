class Stock:
    def __init__(self, stock_dict):
        self.script_name = stock_dict['script_name']
        self.previous_close = stock_dict['previous_close']
        self.today_open = stock_dict['today_open']
        self.prev_close = stock_dict['prev_close']
        self.open_price = stock_dict['open_price']
        self.high_price = stock_dict['high_price']
        self.low_price = stock_dict['low_price']
        self.last_price = stock_dict['last_price']
        self.close_price = stock_dict['close_price']
        self.avg_price = stock_dict['avg_price']
        self.ttl_trd_qnty = stock_dict['ttl_trd_qnty']
        self.turnover_lacs = stock_dict['turnover_lacs']
        self.no_of_trades = stock_dict['no_of_trades']
        self.deliv_qty = stock_dict['deliv_qty']
        self.deliv_per = stock_dict['deliv_per']

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
