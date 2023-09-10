import json
import redis


class RedisPriorityQueue(object):

    SECTION = 'scrapyq'

    def __init__(self, config, collection):
        settings = dict(config.items(self.SECTION, ()))

        queue_prefix = settings.get('queue_prefix', 'scrapyq.queue.')
        redis_db = settings.get('redis_db', 0)
        redis_host = settings.get('redis_host', 'localhost')
        redis_port = settings.get('redis_port', 6379)
        redis_username = self.get_optional_config(settings, 'redis_username')
        redis_password = self.get_optional_config(settings, 'redis_password')

        self.conn = redis.Redis(
            host=redis_host,
            port=int(redis_port),
            encoding="utf-8",
            decode_responses=True,
            db=int(redis_db),
            username=redis_username,
            password=redis_password
        )

        self.queue = f"{queue_prefix}{collection}"

    @staticmethod
    def get_optional_config(settings, name):
        value = settings.get(name, None)
        if value is None:
            return None
        return value.strip('\'').strip('"')

    @staticmethod
    def encode(obj):
        return json.dumps(obj)

    @staticmethod
    def decode(text):
        return json.loads(text)

    def put(self, message, priority=0.0):
        self.conn.zincrby(self.queue, priority, self.encode(message))

    def pop(self):
        try:
            item = self.conn.zrevrange(self.queue, 0, 0)[0]
            if self.conn.zrem(self.queue, item) == 1:
                item = self.decode(item)
                return item
        except IndexError:
            pass

    def remove(self, func):
        count = 0
        for msg in self.conn.zrange(self.queue, 0, -1):
            if func(self.decode(msg)):
                self.conn.zrem(self.queue, msg)
                count += 1
        return count

    def clear(self):
        self.conn.delete(self.queue)

    def __len__(self):
        return self.conn.zcard(self.queue)

    def __iter__(self):
        return (
            (self.decode(obj[0]), obj[1])
            for obj in
            self.conn.zrange(name=self.queue, start=0, end=-1, withscores=True)
        )
