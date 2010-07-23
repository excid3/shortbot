#!/usr/bin/env python
"""
   ShortBot

   A minimal IRC bot for shortening urls with bit.ly

   Written by Chris Oliver

   Includes python-irclib from http://python-irclib.sourceforge.net/

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA   02111-1307, USA.
"""


__author__ = "Chris Oliver <excid3@gmail.com>"
__version__ = "0.1.1"
__date__ = "07/23/2010"
__copyright__ = "Copyright (c) Chris Oliver"
__license__ = "GPL2"


import bitly
import irclib


class ShortBot:
    # Connection information
    network = 'irc.freenode.net'
    port = 6667
    network_pass = ''
    channels = ['#keryx']
    nick = 'Shortybot'
    name = 'Shortybot'
    nick_pass = ''
    
    bitly_user = ""
    bitly_apikey = ""

    msg = "%s posted link \"%s\": %s"

    def __init__(self):
        if not self.bitly_user or not self.bitly_apikey:
            print "You forgot to configure your Bit.ly username and API key dummy...\nEdit shortbot.py to fix this."
            import sys
            sys.exit(1)
    
        self.api = bitly.Api(login=self.bitly_user, apikey=self.bitly_apikey)

        # Create an IRC object
        self.irc = irclib.IRC()

        # Setup the IRC functionality we want to log
        self.irc.add_global_handler('privmsg', self.handlePrivMessage)
        self.irc.add_global_handler('invite', self.handleInvite)
        
        # Create a server object, connect and join the channel
        self.server = self.irc.server()
        self.server.connect(self.network, self.port, 
                            self.nick, ircname=self.name, password=self.network_pass)
        self.server.privmsg("nickserv", "identify %s" % self.nick_pass)
        for channel in self.channels:
            self.server.join(channel)

        # Jump into an infinte loop
        self.irc.process_forever()

    def handleInvite(self, connection, event):
        """ User invites bot to join channel """
        connection.join(event.arguments()[0])    

        
        user = event.source()
    def handlePrivMessage(self, connection, event):
        text = event.arguments()[0]
        
        # Only attempt if its a valid url
        if text.startswith("http://"):
            
            # Shorten
            short = self.api.shorten(text, {'history':1})
            info = self.api.info(short)
            
            print "Shortening %s to %s" % (text, short)
            
            # Send to channel
            for chan in self.channels:
                self.server.privmsg(chan, self.msg % (irclib.nm_to_n(user), info["htmlTitle"], short))
                   

if __name__ == "__main__":
    bot = ShortBot()
    
    
