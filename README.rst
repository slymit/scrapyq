scrapyq
=======

Scrapyq is designed to replace the SQLite backend by a Redis backend.
In other words, all the queue management will be done using Redis.

Scrapyq is a fork of the original
https://github.com/speakol-ads/scrapyd-redis implementation.


Install
-------

.. code-block::

    pip install scrapyq


Config
------

To start using this library you just need to override
the ``spiderqueue`` option in your ``scrapyd.conf`` file:

.. code-block::

    [scrapyd]
    spiderqueue = scrapyq.spiderqueue.RedisSpiderQueue
    ...

If you want to customize the access to the database,
you can add into your ``scrapyd.conf`` file:

.. code-block::

    [scrapyq]
    queue_prefix = scrapyq.queue.
    redis_db = 0
    redis_host = localhost
    redis_port = 6379
    redis_username = 'admin'  # (Optional)
    redis_password = 'password'  # (Optional)
    ...
