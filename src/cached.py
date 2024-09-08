import functools
import json
import redis
import logging

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


def cached(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__

        function_name = func.__name__

        positional_args = "_".join(map(str, args))

        keyword_args = "_".join(f"{k}_{v}" for k, v in kwargs.items())

        key_parts = [class_name, function_name, positional_args, keyword_args]
        key = "_".join(filter(None, key_parts))

        try:
            cached_result = json.loads(redis_client.get(key))
            logging.info(f"Found {key} on redis")
            return cached_result
        except redis.exceptions.ConnectionError:
            logging.exception("Redis service is not active")
        except TypeError:
            logging.info(f"Key {key} not found")
        except Exception as e:
            logging.exception(e)

        result = func(self, *args, **kwargs)

        redis_client.set(key, json.dumps(result))

        return result

    return wrapper
