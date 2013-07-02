# -*- coding: utf-8 -*-

import socket
import time


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from logbook import Logger
import msgpack

log = Logger(__name__)


class GrammeServer(DatagramProtocol):

    def __init__(self, handler):
        self._handler = handler

    def datagramReceived(self, datagram, address):
        data = msgpack.unpackb(datagram)
        log.info('Recieved message from: {0}'.format(str(address)))
        log.debug(dict(raw=datagram, data=data, socket=address))
        return self._handler(data)


def server(host="", port=0):

    def wrapper(fn):

        log.info('Starting up server: {0}:{1}'.format(host, port))
        reactor.listenUDP(port, GrammeServer(fn))
        reactor.run()
        return fn

    return wrapper


class GrammeClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        packaged = msgpack.packb(data)
        log.info('Sending data to: {0}:{1}'.format(self.host, self.port))
        log.debug(dict(raw=data, packaged=packaged, host=self.host, port=self.port))
        self._sock.sendto(packaged, (self.host, self.port))

client = GrammeClient


@server(3030)
def data_handler(data):
    print data

