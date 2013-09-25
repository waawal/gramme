# -*- coding: utf-8 -*-

import socket
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from logbook import Logger
import msgpack

log = Logger('gramme', level='NOTICE')


class GrammeUDPHandler(socketserver.BaseRequestHandler):
    """ Unpacks the data and pass it down to the registered handler. """

    def handle(self):
        raw, sock = self.request
        unpacked = msgpack.unpackb(raw)
        log.info('Recieved message from: {0}'.format(str(sock)))
        log.debug(dict(raw=raw, unpacked=unpacked, socket=sock))
        return GrammeUDPHandler._handler(unpacked)

class GrammeTCPHandler(socketserver.StreamRequestHandler):
    """ Unpacks the data and pass it down to the registered handler. """

    def handle(self):
        raw, sock = self.request
        unpacked = msgpack.unpackb(raw)
        log.info('Recieved message from: {0}'.format(str(sock)))
        log.debug(dict(raw=raw, unpacked=unpacked, socket=sock))
        return GrammeTCPHandler._handler(unpacked)

class GrammeMulticastHandler(socketserver.BaseRequestHandler):
    """ Unpacks the data and pass it down to the registered handler. """

    def handle(self):
        raw, sock = self.request
        unpacked = msgpack.unpackb(raw)
        log.info('Recieved message from: {0}'.format(str(sock)))
        log.debug(dict(raw=raw, unpacked=unpacked, socket=sock))
        return GrammeMulticastHandler._handler(unpacked)

class GrammeServer(object):

    def __init__(self, transport='udp', port=0, host=''):
        self.transport = transport
        self.port = port
        self.host = host

    def start_server(self):
        GrammeUDPHandler._handler = staticmethod(fn)
        _server = socketserver.UDPServer((host, int(port)), GrammeHandler)
        log.notice('Starting server on: {0}:{1}'.format(*_server.server_address))
        try:
            _server.serve_forever()
        except KeyboardInterrupt:
            log.notice('Shutting down server')
            _server.shutdown()
    @classmethod
    def udp(cls, port=0, host=''):
        return cls(transport='udp', port=port, host=host)

    @classmethod
    def tcp(cls, port=0, host=''):
        return cls(transport='tcp', port=port, host=host)

    @classmethod
    def multicast(cls, port=0, host=''):
        return cls(transport='multicast', port=port, host=host)

def udp(port=0, host=''):
    """ Register a callable as a handler. """
    def _wrapper(fn):
        
        return fn
    return _wrapper

def tcp(port=0, host=''):
    """ Register a callable as a handler. """
    def _wrapper(fn):
        
        return fn
    return _wrapper

def multicast(port=0, host=''):
    """ Register a callable as a handler. """
    def _wrapper(fn):
        
        return fn
    return _wrapper



class GrammeClient(object):
    """ Packs and sends data down a socket """

    def __init__(self, port, host='', transport='udp'):
        self.host = host
        self.port = int(port)
        if transport in ('udp', 'datagram', 'dgram', 'datagramme'):
            self._transport = 'udp'
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self._transport = 'tcp'
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data):
        packaged_data = msgpack.packb(data)
        log.info('Sending data to: {0}:{1}'.format(self.host, self.port))
        log.debug(dict(raw=data, packaged_data=packaged_data,
                       host=self.host, port=self.port))
        if self._transport == 'udp':
            self._sock.sendto(packaged_data, (self.host, self.port))
        elif self._transport == 'tcp':
            self._sock.connect((self.host, self.port))
            self._sock.send(packaged_data)
            self._sock.close()

    @classmethod
    def tcp(cls, port, host=''):
        return cls(port, host=host, transport='tcp')

    @classmethod
    def udp(cls, port, host=''):
        return cls(port, host=host, transport='udp')

    @classmethod
    def multicast(cls, port, host=''):
        return cls(port, host=host, transport='multicast')


client = GrammeClient
