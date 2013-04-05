
import ogdConv.inElements.shapefile
from osm2python.tree import Node



class shape:

    def __init__(self,params):
        self.encoding=params.get('encoding','utf-8')

    def gen(self,file):
        self.reader = ogdConv.inElements.shapefile.Reader(encoding=self.encoding,**file)
        avid=0
        for r in self.reader.shapeRecords():
            avid-=1
            if r.shape.shapeType == 1:
                yield { 'name':'node',
                        'attrs':{
                            'lat':r.shape.points[0][0],
                            'lon':r.shape.points[0][1],
                            'id': avid
                            },
                        'children':[{'name':'tag', 'attrs':{'k':x[0],'v':r.record[idx-1]}} for idx,x in enumerate(self.reader.fields)  if x[0]  not in ('DeletionFlag','XCoord','YCoord')]
                        }
            else:
                raise Exception("Unknown shape type %d" % r.shape.type)
