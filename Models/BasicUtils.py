class BasicUtils:
    def __init__(self):
        pass

    def __call__(self,Conv,Irc):
        priv,count,person,place,sent=Conv.last()   

        if sent == 'BYE':
            Irc.quit()
            return 'BYE'
        if sent == 'DUMP': Conv.dump()
        if sent == 'OP' and priv == False:
            Irc.names(place)
            data=Irc()
            dataVect=data.split('\r\n')
            for d in dataVect:
                if d:
                    message=d.split(":")[2]
                    if message != "End of /NAMES list.":
                        for name in message.split():
                            if not name.startswith('@'):
                                Irc.op(place,name)
        return ""

