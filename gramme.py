# -*- coding: utf-8 -*-

import socket
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from logbook import Logger
import msgpack

log = Logger('gramme', level='NOTICE')


class GrammeHandler(socketserver.BaseRequestHandler):
    """ Unpacks the data and pass it down to the registered handler. """

    def handle(self):
        raw, sock = self.request
        unpacked = msgpack.unpackb(raw)
        log.info('Recieved message from: {0}'.format(str(sock)))
        log.debug(dict(raw=raw, unpacked=unpacked, socket=sock))
        return GrammeHandler._handler(unpacked)


def server(port=0, host=""):
    """ Register a callable as a handler. """
    def wrapper(fn):
        GrammeHandler._handler = staticmethod(fn)
        _server = socketserver.UDPServer((host, int(port)), GrammeHandler)
        log.notice('Starting server on: {0}:{1}'.format(*_server.server_address))
        try:
            _server.serve_forever()
        except KeyboardInterrupt:
            log.notice('Shutting down server')
            _server.shutdown()
        return fn
    return wrapper


class GrammeClient(object):
    """ Packs and sends data down a socket """

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