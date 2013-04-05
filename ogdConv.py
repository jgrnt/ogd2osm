
from ogdConv import pipeline
import json
import sys

for a in sys.argv[1:]:
    with open(a, 'r') as f:
        pipeline(json.load(f))

     
