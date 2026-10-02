import re
import time

class Service:
    def __init__(self):
        self.cache = {}

    def run(self, value: str):
        key = re.sub(r"\s+", " ", value.strip().lower())
        item = self.cache.get(key)
        hit = bool(item and item["expires_at"] > time.time())
        if not hit:
            self.cache[key] = {"value": value.upper(), "expires_at": time.time() + 60}
        return {"cache_hit": hit, "value": self.cache[key]["value"], "key": key}
