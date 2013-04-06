import os.path
from functools import reduce
import sys
import ogdConv
import urllib



class pipeline(object):
    
    def __init__(self,params):
        inpipe=self.str_to_class("ogdConv.inElements."+params['input']['type'])(params['input'])
        data=inpipe.gen(self.parseFileParam(params['input']['file']))
        if('preproc' in params):
            data=self.applyfilter(params['preproc'],data)
        if 'mapping' in params:
            data=[self.mapdata(d,params['mapping']) for d in data] 
        if('postproc' in params):
            data=self.applyfilter(params['postproc'],data)
        

        outpipe=self.str_to_class("ogdConv.outElements."+params['output']['type'])(params['output'])
        outpipe.write(data)

    def applyfilter(self,params,data):
        if hasattr(params,'__iter__') and not hasattr(params,'keys') :
            d=data
            for i in params:
                d=self.applyfilter(i,d)
            return d
        else:
            val=self.str_to_class("ogdConv.filter."+params['type'])(**params)
            return val.gen(data)
        
    def mapdata(self,dataItem,mapping):
        dataItem.tags={mapping[k]:v for k,v in dataItem.tags.items() if k in mapping}
        return dataItem
    
    def str_to_class(self,str):
        return reduce(getattr, str.split("."), sys.modules[__name__])

    def parseFileParam(self,fileParam):
        if hasattr(fileParam,'__iter__') and not hasattr(fileParam,'keys') :
           return dict (( self.parseFileItem(f) for f in fileParam))
        return self.parseFileItem(fileParam)

    def parseFileItem(self,f):
        if hasattr(f, 'keys'):
            inputstream=None
            ext=None
            if f.get('filename',None)!=None:
                inputstream=open(f['filename'], 'rb')
                ext= os.path.splitext(f['filename'])[1][1:]
            if f.get('url',None)!=None:
                (temp,_)=urllib.request.urlretrieve(f.get('url'))
                inputstream=open(temp,'rb')
                ext=f.get('ext',ext)
                
            if f.get('type',None)!=None:
                fileconv=(self.str_to_class("ogdConv.file."+f['type']))(f)
                return fileconv.read(inputstream)
            if inputstream == None:
                raise Exception("emtpy file element %s" % f)
            return ext,inputstream
        else:
            return os.path.splitext(f)[1][1:],open(f, 'rb')
        
        
        
            
