import time
from collections import defaultdict
from typing import Callable


def throttle(cooldown: float = 2.0) -> Callable[[str], bool]:
    """
    Returns a function that accepts a key (e.g., object label)
    and returns True only if at least `cooldown` seconds have
    passed since that key was last seen.
    """
    last_time = defaultdict(lambda: 0.0)

    def _inner(key: str) -> bool:
        now = time.time()
        if now - last_time[key] >= cooldown:
            last_time[key] = now
            return True
        return False

    return _inner
