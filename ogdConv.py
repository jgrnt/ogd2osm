
from ogdConv import pipeline
import json
import sys

with open(sys.argv[1], 'r') as f:
    pipeline(json.load(f))

     
