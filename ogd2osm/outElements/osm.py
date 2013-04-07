from osm2python import dump_osm


class osm:

    def __init__(self,param):
        self.filename=param['filename']


    def write(self,gen):
        with open(self.filename, 'w') as f:
            dump_osm(f, [g.as_dict for g in gen] )
        
            
