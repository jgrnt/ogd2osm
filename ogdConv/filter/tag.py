
class tag(object):

    def __init__(self,key,value,**kwargs):
       self.key=key
       self.value=value
                
    def gen(self,data):
        for d in data:
            d.tags[self.key]=self.value
            yield d
