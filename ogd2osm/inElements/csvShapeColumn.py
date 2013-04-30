
from .shapefile import *
from osm import pyosm
import re


class csvShapeColumn:

    def __init__(self,params):
        self.encoding=params.get('encoding','utf-8')
        self.pointRE=re.compile("POINT \(([0-9.]*) ([0-9.]+)\)") 

    def gen(self,f):
        file=f[1]
        l=file.readline().decode(self.encoding).rstrip()
        print(l)
        cols=l.split(",")
        l=file.readline().decode(self.encoding).rstrip()
        avid=0
        while l:
            avid-=1
            vals=l.split(",")
            shapeStr= vals[cols.index("SHAPE")]
            res=re.search(self.pointRE,shapeStr)
            if res:
                
                n=pyosm.Node({
                            'lat':res.group(2),
                            'lon':res.group(1),
                            'id': str(avid)
                            },tags={k:v for k,v in zip(cols,vals)  if k  not in ('SHAPE') })
                yield n
            else:
                raise Exception("Unknown shape type %d" % r.shape.type)
            l=file.readline().decode(self.encoding).rstrip()
