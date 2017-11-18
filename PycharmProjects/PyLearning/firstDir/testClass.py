class myClass:
    def __init__(self, col1, col2):
        self.col1 = col1
        self.col2 = col2

    def __str__(self):
        return "({},{})".format(self.col1, self.col2)

    def __repr__(self):
        return "myClass({coln},{colm})".format(coln=self.col1, colm=self.col2)
        # return "myClass({},{})".format(self.col1, self.col2)
    ''' we have two formats for format *args and **kwargs
    which can be used for printing. args is just positional and kwargs is name value pair.
    '''