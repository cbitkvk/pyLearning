from html.parser import HTMLParser


class StockHtmlParser(HTMLParser):
    def __init__(self, convert_charrefs=True):
         # super(HTMLParser).__init__(convert_charrefs=True)
        self.tr_count = 0
        self.tbody_count = 0
        self.column_count = 0
        self.top_count = 0
        self.stock_dict = dict()
        self.header_names = list()
        self.rawdata = ""
        self.offset = 0
        self.convert_charrefs = convert_charrefs
        self.cdata_elem = None
        self.lasttag = '???'
        self.interesting = None
        self.lineno = 0

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'table':
            self.top_count += 1
        if tag == "tr":
            self.tr_count += 1
            # Not the ideal way, but i am resetting the column count to 0
            # so that we can access column/header names while reading data
            self.column_count = 0
        if tag == "tbody":
            self.tbody_count += 1
        if tag in ["td", "th"]:
            self.column_count += 1

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        print("Encountered some data  :", data)
        if self.tr_count == 1:
            self.stock_dict[data] = None
            self.header_names.append(data)
        else:
            self.stock_dict[self.header_names[self.column_count]] = data
        print(self.stock_dict)

    def close(self):
        return self.stock_dict
