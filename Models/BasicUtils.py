class BasicUtils:
    def __init__(self):
        pass

    def __call__(self,Conv):
        priv,count,person,place,sent=Conv.last()   

        if sent == "BYE": return ('action','BYE')
        if sent == "DUMP": Conv.dump()
        return ('None','None')
