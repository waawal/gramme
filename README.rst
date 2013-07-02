======
gramme
======

A elegant way to pass volatile data around over `UDP (datagrammes) <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_ serialized in `msgpack <http://msgpack.org/>`_

Example Server
--------------
::

    from gramme import server

    @server(3030)
    def handler(data)
        print data

Example Client
--------------
::

    from gramme import client

    clnt = client(host="132.23.x.x", port=3030)

    some_data = {'i am': 'a dict'}
    more_data = 432

    clnt.send(some_data)
    clnt.send(more_data)


Installation
------------

Install *gramme* with pip:

::

    $ pip install greenbalance