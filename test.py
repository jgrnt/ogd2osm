from ogdConv import *

pipeline({
    'input':{
        'type':inElements.shape,
        'filename': 'apotheken.shp'
        },
    #'preproc':{},
    'mapping':{
        'OBJECTID':'ref:ogdgraz',
        'NAME':'name'
        },
    #'postproc':{},
    'output':{
        'type':outElements.osm,
        'filename': 'out.osm'
        }
    })
     
