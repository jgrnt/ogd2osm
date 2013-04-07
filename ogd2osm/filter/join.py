import re

class join(object):

    def __init__(self,key1,key2,newkey,**kwargs):
        self.key1=key1
        self.key2=key2
        self.newkey=newkey
        self.join=kwargs.get("join","%s %s")
        if "value1" in kwargs:
            self.val1=re.compile(kwargs["value1"])
        if "value2" in kwargs:
            self.val2=re.compile(kwargs["value2"])
                
    def gen(self,data):
        for d in data:
            if self.key1 in d.tags and self.key2 in d.tags:
                try:
                    val1=self.val1.findall(d.tags[self.key1])[-1]
                except AttributeError:
                    val1=d.tags[self.key1]
                try:
                    val2=self.val2.findall(d.tags[self.key2])[0][-1]
                except AttributeError:
                    val2=d.tags[self.key2]
                d.tags[self.newkey]=self.join % (val1,val2)
            yield d
            
