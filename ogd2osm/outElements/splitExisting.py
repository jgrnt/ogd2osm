import urllib.request
import json
import sys

from osm import pyosm


class splitExisting:

    def __init__(self,filename,exisiting_filename,query):
        self.filename=filename
        self.query=query
        self.existing_filename=exisiting_filename


    def write(self,gen):
        with open(self.filename, 'w') as f:
            with open(self.existing_filename, 'w') as e:            
                ex=pyosm.OSMXMLFile()             
                notF=pyosm.OSMXMLFile()
                for g in gen:
                    if isinstance(g, pyosm.Node): 
                        sys.stdout.write("\r%d" %g.id)
                        quer=self.query % (g.lat,g.lon)
                        #print(quer)
                        temp=urllib.request.urlopen(quer)
                        A=json.loads(temp.readall().decode())
                        if A["elements"]:
                            ex.nodes[g.id]=g
                        else :
                            notF.nodes[g.id]=g
                ex.write(e)
                notF.write(f)
