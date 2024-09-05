import redis
import logging
import requests
import json

r = redis.Redis(host='redis', port=6379, decode_responses=True)

class CacheManager:
    
    def __init__(self, URL, API_VERSION):
        self.URL = URL
        self.API_VERSION = API_VERSION

    def get(self, api: str) -> dict:        
        if api.startswith(self.URL):
            full_url = api
        else:
            full_url = '/'.join([self.URL, self.API_VERSION, api])

        is_redis_on = True

        try:
            cache = r.get(full_url)
            cache = json.loads(cache)
            logging.info(f"Found {full_url} on redis")
            return cache
        except redis.exceptions.ConnectionError:
            logging.exception("Redis service is not active")
            is_redis_on = False
        except Exception as e:
            logging.exception(e)            
        
        logging.info(f"Sending API request to {full_url}")
        response = requests.get(full_url)
        response = response.json()
        
        logging.info(f"Storing cache for {full_url}")

        if is_redis_on:
            r.set(full_url, json.dumps(response))

        return response

