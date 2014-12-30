import socket

class Irc:
    def __init__(self,name='OtterBot',network='127.0.0.1',port=6667):
        self.name=name
        self.network=network
        self.port=port

        self.conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __call__(self):
        return self.conn.recv( 4096 )
        

    def connect(self,name=None,network=None,port=None):
        if name: self.name=name
        if network: self.network=network
        if port: self.port=port

        self.conn.connect( (self.network,self.port) )
        self.conn.recv( 4096 )
        self.conn.send( 'NICK %s\r\n' % self.name )
        self.conn.send( 'USER %s %s %s :Python IRC\r\n' % (self.name, self.name, self.name))

    def join(self,channel=None):
        if not channel: return
        self.conn.send( 'JOIN %s\r\n' % channel )

    def privmsg(self,channel=None,message=None):
        if not channel: return None
        if not message: return None
        self.conn.send( 'PRIVMSG %s : %s\r\n' % (channel,message) )

    def names(self,channel=None):
        if not channel: return None
        self.conn.send( 'NAMES %s\r\n' % channel )

    def op(self,channel=None,person=None):
        if not channel: return
        if not person: return
        self.conn.send( 'MODE %s +o %s\r\n' % (channel,person) )

    def quit(self):
        self.conn.send( 'QUIT meh...\r\n' )
