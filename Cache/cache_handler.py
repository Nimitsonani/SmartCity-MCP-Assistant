import json
import time

class Cache:
    def __init__(self):
        self.cache={}
        with open('Cache/cache.json','r') as f:
            self.cache=json.load(f)

    def add(self,key,value):
        self.cache[key]={f"time":time.time(),
                         "data":value}

        with open('Cache/cache.json','w') as f:
            json.dump(self.cache,f)

cache = Cache()