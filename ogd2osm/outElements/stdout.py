



class stdout:

    def __init__(self):
        pass
    
    def write(self, gen):
        for a in gen:
            print(a)
