import time

cache_store = {}

CACHE_TTL = 60  # seconds


def get_cache(key: str):
    data = cache_store.get(key)

    if not data:
        return None

    value, expiry = data

    if time.time() > expiry:
        del cache_store[key]
        return None

    return value


def set_cache(key: str, value):
    expiry = time.time() + CACHE_TTL
    cache_store[key] = (value, expiry)


def clear_doctor_cache():
    keys = list(cache_store.keys())
    for key in keys:
        if key.startswith("doctors:"):
            del cache_store[key]