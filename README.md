# scrapyq

[![version](https://img.shields.io/pypi/v/scrapyq.svg)](https://pypi.python.org/pypi/scrapyq)
[![pyversions](https://img.shields.io/pypi/pyversions/scrapyq.svg)](https://pypi.python.org/pypi/scrapyq)
[![actions](https://github.com/slymit/scrapyq/actions/workflows/python-test.yml/badge.svg)](https://github.com/slymit/scrapyq/actions/workflows/python-test.yml)
[![codecov](https://codecov.io/github/slymit/scrapyq/graph/badge.svg?token=EYCSS4IG5F)](https://codecov.io/github/slymit/scrapyq)

Scrapyq is designed to replace the SQLite backend by a Redis backend.
In other words, all the queue management will be done using Redis.

Scrapyq is a fork of the original
<https://github.com/speakol-ads/scrapyd-redis> implementation.

## Install

```shell
pip install scrapyq
```

## Config

To start using this library you just need to override
the `spiderqueue` option in your `scrapyd.conf` file:

```ini
[scrapyd]
spiderqueue = scrapyq.spiderqueue.RedisSpiderQueue
```

If you want to customize the access to the database,
you can add into your `scrapyd.conf` file:

```ini
[scrapyq]
queue_prefix = scrapyq.queue.
redis_db = 0
redis_host = localhost
redis_port = 6379
redis_username = 'admin'  # (Optional)
redis_password = 'password'  # (Optional)
```
