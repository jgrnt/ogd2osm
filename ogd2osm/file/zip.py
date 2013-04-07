import os
import tempfile
from zipfile import ZipFile


class zip(object):

    def __init__(self,params):
        pass
    def read(self,stream):
        t=ZipFile(stream)
        with tempfile.TemporaryDirectory() as tmpdir:
            t.extractall(tmpdir)
            return { os.path.splitext(f)[1][1:]:open(tmpdir+"/"+f,"rb") for f in t.namelist()}
