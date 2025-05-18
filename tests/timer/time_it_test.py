# file: time_it_test.py

import unittest
import asyncio
from common_util.timer import time_it, async_time_it

class TimeitTest(unittest.TestCase):

    def test_01(self) -> None:
        self.for_loop_test()
        return

    def test_02(self) -> None:
        asyncio.run(self.async_for_loop_test())
        return
    
    def test_03(self) -> None:
        asyncio.run(self.async_sleep())
        return

    @time_it()
    def for_loop_test(self) -> None:
        for _ in range(1000000):
            pass
        return

    @async_time_it()
    async def async_for_loop_test(self) -> None:
        for _ in range(1000000):
            pass
        return
    
    @async_time_it()
    async def async_sleep(self) -> None:
        sec_count: int = 2
        print(f'sleeping for {sec_count} seconds')
        await asyncio.sleep(sec_count)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
