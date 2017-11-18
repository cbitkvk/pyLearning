class HelloWorld:

    def __init__(self,name = "no name", how_to_address = "dont address me"):
        self.name = name
        self.how_to_address = how_to_address

    def __call__(self):
        return "you are calling an callable instance of class"

    def __str__(self):
        return str({"name" : self.name , "how_to_address" : self.how_to_address})

    def set_values(self,*args):
        self.name = args[0]
        self.how_to_address = args[1]

    def set_values(self,**kwargs):
        self.name = kwargs[name]
        self.how_to_address = kwargs[how_to_address]

    def get_values(self,field):
        return {"name" : self.name , "how_to_address" : self.how_to_address}
