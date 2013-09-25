======
gramme
======

.. image:: https://badge.fury.io/py/gramme.png
    :alt: pypi version
    :align: left
    :target: https://pypi.python.org/pypi/gramme

A elegant way to pass volatile data around over `UDP (datagrammes) <https://en.wikipedia.org/wiki/User_Datagram_Protocol>`_ serialized with `msgpack <http://msgpack.org/>`_

Example Server
--------------

.. code:: python

    import gramme

    @gramme.server(3030)
    def my_awsome_data_handler(data):
        print data

Example Client
--------------

.. code:: python

    import gramme

    client = gramme.client(host="132.23.x.x", port=3030)

    some_data = {'key': 'value'}
    client.send(some_data)

    more_data = ['i am a list', 1, {'hello': 'there!'}]
    client.send(more_data)


Installation
------------

Install *gramme* with pip:

::

    $ pip install gramme


License
-------

BSD
