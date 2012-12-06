#!/usr/bin/env python


import json
import logging

import psutil

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from autobahn.websocket import (listenWS, WebSocketServerFactory,
                                WebSocketServerProtocol)


logging.basicConfig(level=logging.DEBUG)


class CPUWebSocketServerFactory(WebSocketServerFactory):

    cpu_usage = []

    def __init__(self, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs)
        self.clients = []

    def _updateUsage(self):
        self.cpu_usage = psutil.cpu_percent(percpu=True)
        for client in self.clients:
            client.sendUsage()

    def startFactory(self):
        lc = LoopingCall(self._updateUsage)
        lc.start(1, now=True)


class CPUWebSocketServerProtocol(WebSocketServerProtocol):

    def connectionMade(self):
        WebSocketServerProtocol.connectionMade(self)
        logging.info('Connection made from %s!', self.peerstr)
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        logging.info('Connection lost from %s!', self.peerstr)
        self.factory.clients.remove(self)

    def onMessage(self, msg, binary):
        logging.info('%s said "%s", cool right?', self.peerstr, msg)

    def sendUsage(self):
        usage = json.dumps(self.factory.cpu_usage)
        self.sendMessage(usage)


if __name__ == '__main__':
    url = 'ws://localhost:9000'

    factory = CPUWebSocketServerFactory(url)
    factory.protocol = CPUWebSocketServerProtocol
    listenWS(factory)
    logging.info('Listening on %s', url)

    reactor.run()
