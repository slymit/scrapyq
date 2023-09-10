from zope.interface import implementer
from scrapyd.interfaces import ISpiderQueue
from scrapyq.redis import RedisPriorityQueue


@implementer(ISpiderQueue)
class RedisSpiderQueue(object):

    def __init__(self, config, collection):
        self.q = RedisPriorityQueue(config, collection)

    def add(self, name, priority=0.0, **spider_args):
        d = spider_args.copy()
        d['name'] = name
        self.q.put(d, priority=priority)

    def pop(self):
        return self.q.pop()

    def count(self):
        return len(self.q)

    def list(self):
        return [x[0] for x in self.q]

    def remove(self, func):
        return self.q.remove(func)

    def clear(self):
        self.q.clear()
