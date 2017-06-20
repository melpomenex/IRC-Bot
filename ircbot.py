#!/usr/bin/python3
import socket
import re
from exchanges.bitfinex import Bitfinex



ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = #"irc server goes here" # Server
channel = #"channel you want to join goes here" # Channel
botnick = #"bot nick goes here"
adminname = #"admin name goes here"
exitcode = "bye " + botnick
port = 6667
bitcoin_price = Bitfinex().get_current_price()



class BOT():
    def __init__(self, server, port, botnick, adminname, channel=None):
		#channel=None allows you to not necessarily provide a value for this argument
        self.SERVER = server
        self.PORT = port
        self.BOTNICK = botnick
        self.ADMINNAME = adminname
        self.CHANNEL = channel
        self._IRCSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connected = self._connect()


    def _connect(self):
        self._IRCSOCK.connect((self.SERVER, self.PORT))
        self._IRCSOCK.send(bytes("USER "+ self.BOTNICK +" "+ self.BOTNICK +" "+ self.BOTNICK + " " + self.BOTNICK + "\n", "UTF-8"))
        self._IRCSOCK.send(bytes("NICK "+ self.BOTNICK +"\n", "UTF-8")) # assign the nick to the bot

    def _ping(self):
        ''' responds to a ping request from the server '''
        self._IRCSOCK.send(bytes("PONG :pingis\n", "UTF-8"))

    def _getusers(self):
        ''' gets the users in the channel '''
        self_IRCSOCK.send(bytes("/NAMES "+ self.channel +"\n", "UTF-8"))
        ircmsg = ""
        while ircmsg.find("End of /NAMES list.") == -1:
            ircmsg += self._IRCSOCK.recv(2048).decode("UTF-8").strip('\n\r')
            print("TEST LIST OF USERS", ircmsg)

    def joinchan(self):
        ''' Joins the channel '''
        self._IRCSOCK.send(bytes("JOIN "+ self.CHANNEL +"\n", "UTF-8"))

    def sendmsg(self, msg):
        self._IRCSOCK.send(bytes("PRIVMSG "+ self.CHANNEL +" :"+ msg +"\n", "UTF-8"))

    def recvmsg(self):
        return self._IRCSOCK.recv(2048).decode("UTF-8").strip('\n\r')

    def _clientinfo(self, user):
        self._IRCSOCK.send(bytes("/CTCP "+user+" clientinfo\n", "UTF-8"))

    def _dccmsg(self, user, msg):
        self._IRCSOCK.send(bytes("/CTCP "+user+" dcc "+msg+"\n", "UTF-8"))

    def _action(self, user, action):
        self._IRCSOCK.send(bytes("/CTCP "+user+" action "+action+"\n", "UTF-8"))




def main():
    # Initialize the bot class as bot
    bot = BOT(server, port, botnick, adminname, channel)
    bot.joinchan()
    bot._ping()
    while 1:
        try:
            ircmsg = bot.recvmsg()
            if ircmsg.find("PING :") != -1:
                bot._ping()
            if ircmsg.find("PRIVMSG") != -1:
                ''' prints the link to sportsbookreview for the nba lines '''
                if "!line" in ircmsg:
                    print("msg", ircmsg)
                    bot.sendmsg("here are the lines for today:" + " http://www.sportsbookreview.com/betting-odds/nba-basketball/")
                    ''' prints the current price of bitcoin in the chat '''
                elif ircmsg.index("!btc") != -1:
                    print("msg", ircmsg)
                    bot.sendmsg(str(bitcoin_price))


        except Exception as e:
            print("ERROR:", e)

main()
