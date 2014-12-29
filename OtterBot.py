#!/usr/bin/env python

import socket
from Util.Conv import Conv

class OtterBot:
    def __init__(self,name='OtterBot',network='127.0.0.1',port=6667):
        self.name=name
        n=name

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect( ( network, port ) )
        self.irc.recv( 4096 )
        self.irc.send( 'NICK %s\r\n' % n )
        self.irc.send( 'USER %s %s %s :Python IRC\r\n'  % (n,n,n))
        self.irc.send( 'JOIN #test\r\n' )

        self.words={}
        self.bigrams={}

        self.targetName=""
        self.message=""

        self.Conv=Conv()

    def __call__(self):
        while True:
           data = self.irc.recv ( 4096 )
           print data.strip()
           if data.find ( 'PING' ) != -1:
              self.irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
           elif data.find ( 'PRIVMSG' ) != -1:
              message = ':'.join ( data.split ( ':' ) [ 2: ] )
              nick = data.split ( '!' ) [ 0 ].replace ( ':', '' )
              destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]

              # TODO: Printing information out to the screen so I can see what's happening.
              # This is temporary and should be removed in the future.
              print "message: %s" % message.strip()
              print "nick: %s" % nick
              print "destination: %s" % destination

              ret=self.processMessage(destination,nick,message)
              if ret == 'BYE':
                  self.Conv.dump()
                  return
              print 50*"-"
              if ret: self.irc.send(ret)

    def processMessage(self,destination,nick,message=None):
        if not message: return None

        # Basically handling a private mesage or a chatroom message
        if destination == self.name:
            self.targetName=nick
            self.priv=True
        else:
            self.targetName=destination
            self.priv=False

        self.message=message.strip()

        self.Conv.add(self.priv,nick,self.targetName,self.message)
        if self.message=='BYE': return 'BYE'
        return ""


if __name__ == "__main__":
    bot=OtterBot(name='OtterBot')
    bot()
