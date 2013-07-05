======
gramme
======

A elegant way to pass volatile data around over `UDP (datagrammes) <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_ serialized with `msgpack <http://msgpack.org/>`_

Example Server
--------------
::

    import gramme

    @gramme.server(3030)
    def my_awsome_data_handler(data):
        print data

Example Client
--------------
::

    import gramme

    client = gramme.client(host="132.23.x.x", port=3030)

    some_data = {'i am': 'a dict'}
    client.send(some_data)

    some_more_data = ['i am a list', 3, 4, {'hello': 'there!'}]
    client.send(some_more_data)


Installation
------------

Install *gramme* with pip:

::

    $ pip install gramme


License
-------

BSD
