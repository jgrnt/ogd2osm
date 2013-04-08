
from osm import pyosm


class osmFile:

    def __init__(self,filename):
        self.filename=filename


    def write(self,gen):
        with open(self.filename, 'w') as f:
            doc=pyosm.OSMXMLFile()
            doc.nodes={str(g.id):g for g in gen if  isinstance(g, pyosm.Node)} 
            doc.write(f)
        
            
