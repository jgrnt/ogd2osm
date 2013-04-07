
from .shapefile import *
from osm import pyosm



class shape:

    def __init__(self,params):
        self.encoding=params.get('encoding','utf-8')

    def gen(self,file):
        self.reader = Reader(encoding=self.encoding,**file)
        avid=0
        for r in self.reader.shapeRecords():
            avid-=1
            if r.shape.shapeType == 1:
                n=pyosm.Node({
                            'lat':r.shape.points[0][1],
                            'lon':r.shape.points[0][0],
                            'id': str(avid)
                            },tags={x[0]:str(r.record[idx-1]) for idx,x in enumerate(self.reader.fields)  if x[0]  not in ('DeletionFlag','XCoord','YCoord') })
                yield n
            else:
                raise Exception("Unknown shape type %d" % r.shape.type)
