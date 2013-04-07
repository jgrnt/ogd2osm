import re

class filterTag(object):

    def __init__(self,key,value,**kwargs):
        self.value_re=re.compile(value)
        self.key_re=re.compile(key)
        

    def gen(self,data):
        for d in data:
            A={k:v for k,v in d.tags.items() if self.key_re.search(k) == None or self.value_re.search(v) == None}
            d.tags=A
            yield d
