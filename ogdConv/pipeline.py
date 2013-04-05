import os.path
from functools import reduce
import sys
import ogdConv



class pipeline(object):
    
    def __init__(self,params):
        inpipe=self.str_to_class("ogdConv.inElements."+params['input']['type'])(params['input'])
        print(self.parseFileParam(params['input']['file']))
        data=inpipe.gen(self.parseFileParam(params['input']['file']))
        if('preproc' in params):
            val=self.str_to_class("ogdConv.inElements."+params['preproc']['type'])(params['preproc'])
            data=val.gen(data)
        data=[self.mapdata(d,params['mapping']) for d in data]
        if('postproc' in params):
            val=self.str_to_class("ogdConv.inElements."+params['postproc']['type'])(params['postproc'])
            data=val.gen(data)  
        outpipe=self.str_to_class("ogdConv.outElements."+params['output']['type'])(params['output'])
        outpipe.write(data)

    def mapdata(self,dataItem,mapping):
        if "children" in dataItem:
            for i in range(len(dataItem["children"]) - 1, -1, -1):
                if dataItem["children"][i]["name"]=="tag":
                    if dataItem["children"][i]["attrs"]["k"] in mapping:
                        dataItem["children"][i]["attrs"]["k"]=mapping[dataItem["children"][i]["attrs"]["k"]]
                    else:
                        del dataItem["children"][i]
                        
                        
                
        return dataItem
    
    def str_to_class(self,str):
        return reduce(getattr, str.split("."), sys.modules[__name__])

    def parseFileParam(self,fileParam):
        if hasattr(fileParam,'__iter__'):
           return dict (( self.parseFileItem(f) for f in fileParam))
        return self.parseFileItem(f)

    def parseFileItem(self,f):
        if hasattr(f, 'keys'):
            inputstream=None
            ext=None
            if f.get('filename',None)!=None:
                inputstream=open(f['filename'], 'rb')
                ext= os.path.splitext(f['filename'])[1][1:]
            if f.get('type',None)!=None:
                pass
            if inputstream == None:
                raise Exception("emtpy file element %s" % f)
            return ext,inputstream
        else:
            return os.path.splitext(f)[1][1:],open(f, 'rb')
        
        
        
            
