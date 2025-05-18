# file: time_it.py

import time
from contextlib import asynccontextmanager, contextmanager

from typing import Generator, AsyncGenerator

@contextmanager
def time_it() -> Generator[None, None, None]:
    now: float = time.monotonic()
    try:
        yield
    finally:
        elasped_time: float = time.monotonic() - now
        print(f'it tooks {elasped_time:.4f} seconds to run')
    return

@asynccontextmanager
async def async_time_it() -> AsyncGenerator[None, None]:
    now: float = time.monotonic()
    try:
        yield
    finally:
        elasped_time: float = time.monotonic() - now
        print(f'it tooks {elasped_time:.4f} seconds to run')
    return

# --- end of file --- #
