import re

class split(object):

    def __init__(self,key,matcher,**kwargs):
        self.key=key
        self.re=re.compile(matcher)
        

    def gen(self,data):
        for d in data:
            if self.key in d.tags:
                try:
                    A={self.key+str(idx+1):v for idx,v in enumerate(re.findall(self.re,d.tags[self.key])[0])}
                    d.tags.update(A)
                except IndexError:
                    pass
            yield d
            
            
