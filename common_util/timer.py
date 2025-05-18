# file: timer.py

import time

from typing import Self, Type, Any
from types import TracebackType

class Timer:

    def __init__(self, name: str) -> None:
        self._name: str = name
        return
    
    def __enter__(self) -> Self:
        self.start_time: float = time.perf_counter()
        print(f'{self.name()} starts at {self.start_time:.4f}')
        return self
    
    def __exit__(self,
                 type: Type[BaseException] | None,
                 value: Any | None,
                 traceback: TracebackType | None) -> bool:
        self.end_time: float = time.perf_counter()
        elapsed_time: float = self.end_time - self.start_time
        print(f'{self.name()} ends at {self.end_time:.4f}')
        print(f'elaspsed time: {elapsed_time:.4f} seconds')
        print(f'exception: {type}, {value}, {traceback}')
        return True
    
    def name(self) -> str:
        return f'Timer("{self._name}")'
    
    @staticmethod
    def main() -> None:
        Timer.test_01_for_loop()
        Timer.test_02_exception()
        return

    @staticmethod
    def test_01_for_loop() -> None:
        with Timer('for loop timer') as timer:
            print(f'running in {timer.name()}')
            for _ in range(1000000):
                pass
        print()
        return
    
    @staticmethod
    def test_02_exception() -> None:
        with Timer('exception in timer') as timer:
            print(f'running in {timer.name()}')
            raise ValueError()        
        print()
        return

if __name__ == '__main__':
    Timer.main()

# --- end of file --- #
