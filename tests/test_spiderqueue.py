from dataclasses import dataclass
import pytest
from twisted.internet.defer import inlineCallbacks, maybeDeferred
from twisted.trial import unittest
from zope.interface.verify import verifyObject
from redis.exceptions import AuthenticationError
from scrapyd.config import Config
from scrapyd.interfaces import ISpiderQueue
from scrapyq.spiderqueue import RedisSpiderQueue


@dataclass
class Spider:
    name: str
    priority: int
    args: dict

    @property
    def msg(self) -> dict:
        msg = self.args.copy()
        msg['name'] = self.name
        return msg


class SpiderQueueTest(unittest.TestCase):
    """This test case also supports queues with deferred methods.
    """

    def setUp(self):
        self.q = RedisSpiderQueue(
            Config(values={'dbs_dir': ':memory:'}), 'quotesbot'
        )
        self.q2 = RedisSpiderQueue(
            Config(extra_sources=('tests/scrapyd.conf',)), 'quotesbot'
        )
        self.spider_1 = Spider(
            'spider1', 5, {'arg1': 'val1', 'arg2': 2, 'arg3': u'\N{SNOWMAN}', }
        )
        self.spider_2 = Spider(
            'spider2', 1, {'arg1': 'val1', 'arg2': None, }
        )

    def test_interface(self):
        verifyObject(ISpiderQueue, self.q)

    @inlineCallbacks
    def test_authentication_error(self):
        with pytest.raises(AuthenticationError):
            yield maybeDeferred(self.q2.count)

    @inlineCallbacks
    def test_add_pop_count(self):
        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 0)

        yield maybeDeferred(
            self.q.add,
            self.spider_1.name,
            self.spider_1.priority,
            **self.spider_1.args
        )
        yield maybeDeferred(
            self.q.add,
            self.spider_2.name,
            self.spider_2.priority,
            **self.spider_2.args
        )

        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 2)

        m = yield maybeDeferred(self.q.pop)
        n = yield maybeDeferred(self.q.pop)
        self.assertEqual(m, self.spider_1.msg)
        self.assertEqual(n, self.spider_2.msg)

        yield maybeDeferred(self.q.pop)

        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 0)

    @inlineCallbacks
    def test_list(self):
        actual = yield maybeDeferred(self.q.list)
        self.assertEqual(actual, [])

        yield maybeDeferred(
            self.q.add,
            self.spider_1.name,
            self.spider_1.priority,
            **self.spider_1.args
        )
        yield maybeDeferred(
            self.q.add,
            self.spider_1.name,
            self.spider_1.priority,
            **self.spider_1.args
        )
        yield maybeDeferred(
            self.q.add,
            self.spider_2.name,
            self.spider_2.priority,
            **self.spider_2.args
        )

        actual = yield maybeDeferred(self.q.list)
        self.assertEqual(actual, [self.spider_2.msg, self.spider_1.msg])

        yield maybeDeferred(self.q.clear)

    @inlineCallbacks
    def test_remove_clear(self):
        yield maybeDeferred(
            self.q.add,
            self.spider_1.name,
            self.spider_1.priority,
            **self.spider_1.args
        )
        yield maybeDeferred(
            self.q.add,
            self.spider_1.name,
            self.spider_1.priority,
            **self.spider_1.args
        )
        yield maybeDeferred(
            self.q.add,
            self.spider_2.name,
            self.spider_2.priority,
            **self.spider_2.args
        )

        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 2)

        yield maybeDeferred(self.q.remove, lambda x: x['name'] == 'spider2')

        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 1)

        yield maybeDeferred(self.q.clear)

        c = yield maybeDeferred(self.q.count)
        self.assertEqual(c, 0)
