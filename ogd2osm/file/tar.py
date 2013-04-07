import os
import tarfile


class tar(object):

    def __init__(self,params):
        pass
    def read(self,stream):
        t=tarfile.open(fileobj=stream)
        return { os.path.splitext(f)[1][1:]:t.extractfile(f) for f in t.getnames()}
