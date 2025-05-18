# file: timer_test.py

import unittest
from common_util.timer import Timer

class TimerTest(unittest.TestCase):

    def test_timer_normal(self) -> None:
        Timer.test_01_for_loop()
        return
    
    def test_timer_expection(self) -> None:
        Timer.test_02_exception()
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
