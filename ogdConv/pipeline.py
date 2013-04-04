

class pipeline(object):
    
    def __init__(self,params):
        inpipe=params['input']['type'](params['input'])
        outpipe=params['output']['type'](params['output'])
        outpipe.write(inpipe.gen())
    
