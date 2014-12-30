#!/usr/bin/env python

import socket
from Util.Conv import Conv
from Util.Irc import Irc
from Models import BasicUtils

class OtterBot:
    def __init__(self,name='OtterBot',network='127.0.0.1',port=6667):
        self.name=name

        self.Irc = Irc(name, network, port)
        self.Irc.connect()
        self.Conv=None
        self.Models=[]

        self.targetName=""
        self.message=""


    def __call__(self):
        while True:
           data = self.Irc()
           print data.strip()
           print 50*"-"
           if data.find ( 'PING' ) != -1:
              self.Irc.conn.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
           elif data.find ( 'PRIVMSG' ) != -1:
              message = ':'.join ( data.split ( ':' ) [ 2: ] )
              nick = data.split ( '!' ) [ 0 ].replace ( ':', '' )
              destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]

              ret=self.processMessage(destination,nick,message)
              if ret == 'BYE': return

    def join(self,channel=None):
        if not channel: return
        self.Irc.join(channel)

    def addConv(self,Conversation):
        self.Conv=Conversation

    def addModel(self,Model):
        self.Models.append(Model)

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


        self.Conv(self.priv,nick,self.targetName,self.message)
        for model in self.Models:
            action=model(self.Conv,self.Irc)
            if action == 'BYE': return 'BYE'
        return ""


if __name__ == "__main__":
    bot=OtterBot(name='OtterBot', network='127.0.0.1', port=6667)
    bot.join('#test')
    bot.addConv(Conv())
    bot.addModel(BasicUtils.BasicUtils())
    bot()
