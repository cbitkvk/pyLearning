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
        if tag == 'tr':
            self.tr_count += 1

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        try:
            if self.tr_count == 1:
                if "\n\t" not in data and ' ' != data:
                    self.stock_dict[data] = None
                    self.header_names.append(data)
            else:
                if self.column_count <= len(self.header_names):
                    if "\n\t" not in data:
                        self.stock_dict[self.header_names[self.column_count - 1]] = data
                        print(data)
                        print(self.header_names[self.column_count-1])
                    # print("column count", self.column_count)
                    # print("header count", len(self.header_names))
                    # self.stock_dict['abc'] =self.column_count
                    print(self.header_names)
        except Exception as p:
            print(self.tr_count)
            print(self.header_names)
            print(self.column_count)

        print(self.stock_dict)

    def close(self):
        return self.stock_dict
