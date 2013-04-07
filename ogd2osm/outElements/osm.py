
from osm import pyosm


class osm:

    def __init__(self,param):
        self.filename=param['filename']


    def write(self,gen):
        with open(self.filename, 'w') as f:
            doc=pyosm.OSMXMLFile()
            doc.nodes={str(g.id):g for g in gen if  isinstance(g, pyosm.Node)} 
            doc.write(f)
        
            
