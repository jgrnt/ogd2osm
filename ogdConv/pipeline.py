

class pipeline(object):
    
    def __init__(self,params):
        inpipe=params['input']['type'](params['input'])
        data=inpipe.gen()
        if('preproc' in params):
            val=params['preproc']['type'](params['preproc'])
            data=val.gen(data)
        data=[self.mapdata(d,params['mapping']) for d in data]
        if('postproc' in params):
            val=params['postproc']['type'](params['postproc'])
            data=val.gen(data)  
        outpipe=params['output']['type'](params['output'])
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
        
            
