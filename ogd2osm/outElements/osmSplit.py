from osm import pyosm,multipolygon
import subprocess
import os
import urllib.request


class osmSplit:

    def __init__(self,query,dirname,**params):
        self.dir=dirname
        if "querycache" in params:
            try:
                self.rels=pyosm.OSMXMLFile(params["querycache"])
            except ValueError:
                urllib.request.urlretrieve(query,filename=params["querycache"])
                self.rels=pyosm.OSMXMLFile(params["querycache"])
        else:
            self.rels=pyosm.OSMXMLFile(content=urllib.request.urlopen(query))    
        try:
            os.mkdir(self.dir)
        except OSError:
            pass
        
            


    def write(self,gen):
        gen=set(gen)
        rels={}
        for rel in self.rels.relations.values():
            mp=multipolygon.multipolygon(rel)
            matches=mp.inside(gen)
            val=set(g for g,i in zip(gen,matches) if i)
            rels[rel]=val
            gen=gen-val
        notfiltered=gen


        for r,elements in rels.items():
            if elements:
                with open(self.dir+"/"+r.tags["name"]+".osm", 'w') as f:
                    doc=pyosm.OSMXMLFile()
                    doc.nodes={str(g.id):g for g in elements if  isinstance(g, pyosm.Node)} 
                    doc.write(f)

        
            
