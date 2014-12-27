#!/usr/bin/env python

import socket

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
              if ret == 'LEAVENOW': return
              print 50*"-"
              if ret: self.irc.send(ret)

    def processMessage(self,destination,nick,message=None):
        if not message: return None

        # This is an old holdover from previous code.  I'll
        # probably be removing all of this self.assoc and self.direct
        # stuff in the future.

        # Basically handling a private mesage or a chatroom message
        if destination == self.name:
            self.targetName=nick
            self.assoc=True    # Am I associated or implicated?
            self.direct=True   # Am I being directly talked to?
        else:
            self.targetName=destination
            self.assoc=False
            self.direct=False

        # Am I being talked directly to (is my name the first word?)
        if message.startswith(self.name):
            self.assoc=True
            self.direct=True
            message=message[message.find(' '):]

        if self.name in message:
            self.assoc=True
        self.message=message.strip()

        # The following if-elsif-else originally handled whether the
        # bot was being talked about, talked directly to, or not involved
        # in a message.
        if self.assoc and not self.direct:
            self.associated()
        elif self.direct:
            self.directed()
            if message=='LEAVENOW': return 'LEAVENOW'
        else:
            self.listening()

    def associated(self):
        """ If the bot is implicated or associated in a sentence somehow, print one of these messages."""
        st=["I've been implicated..."]

        for s in st:
            self.irc.send( 'PRIVMSG %s :%s \r\n' % (self.targetName,s) )

    def directed(self):
        st=["You're talkin to me?"]

        for s in st:
            self.irc.send( 'PRIVMSG %s : %s \r\n' % (self.targetName,s) )

    def listening(self):
        st=["Just listening in..."]
        for s in st:
            self.irc.send( 'PRIVMSG %s : %s \r\n' % (self.targetName,s) )

    def getHelp(self):
        ret=[]
        ret.append('Help Usage:')
        ret.append('  help                - This message')

        return ret


if __name__ == "__main__":
    bot=OtterBot(name='OtterBot')
    bot()
