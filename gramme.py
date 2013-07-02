# -*- coding: utf-8 -*-

import socket
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from logbook import Logger
import msgpack

log = Logger(__name__)


class GrammeHandler(socketserver.BaseRequestHandler):
    """ Unpacks the data and pass it down to the registered handler. """
    def handle(self):
        data = msgpack.unpackb(self.request[0])
        socket = self.request[1]
        log.info('Recieved message from: {0}'.format(str(socket)))
        log.debug(dict(raw=self.request[0], data=data, socket=socket))
        return GrammeHandler._handler(data)


def server(port=0, host=""):
    """ Register a callable as a handler. """
    def wrapper(fn):
        GrammeHandler._handler = staticmethod(fn)
        _server = socketserver.UDPServer((host, int(port)), GrammeHandler)
        log.info('Starting server on: {0}:{1}'.format(*_server.server_address))
        try:
            _server.serve_forever()
        except KeyboardInterrupt:
            log.info('Shutting down server')
            _server.shutdown()
        return fn
    return wrapper


class GrammeClient(object):
    """ Packs and sends data to a socket """
    def __init__(self, port, host=""):
        self.host = host
        self.port = int(port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        packaged = msgpack.packb(data)
        log.info('Sending data to: {0}:{1}'.format(self.host, self.port))
        log.debug(dict(raw=data, packaged=packaged,
                       host=self.host, port=self.port))
        self._sock.sendto(packaged, (self.host, self.port))

client = GrammeClient