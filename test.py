from ogdConv import *

pipeline({
    'input':{
        'type':inElements.shape,
        'filename': 'apotheken.shp'
        },
    'preproc':{},
    'mapping':{},
    'postproc':{},
    'output':{
        'type':outElements.osm,
        'filename': 'out.osm'
        }
    })
     
