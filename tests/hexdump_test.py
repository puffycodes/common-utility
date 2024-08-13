# file: hexdump_test.py

import unittest
from common_util.hexdump import HexDump

class HexDumpTest(unittest.TestCase):

    def test_01(self):
        all_bytes = bytes([v for v in range(256)])
        print(f'-- {HexDump.to_hex(all_bytes)}')
        print(f'-- {HexDump.to_hex(all_bytes, offset=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, pos=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, pos=50, offset=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50, offset=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50, offset=50, pos=50)}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50, offset=240, pos=50)}')
        print()
        print(f'-- {HexDump.to_text(all_bytes)}')
        print(f'-- {HexDump.to_text(all_bytes, offset=32)}')
        return
    
    def test_02(self):
        all_bytes = bytes([v for v in range(256)])
        hexdump_array = HexDump.hexdump(all_bytes)
        print()
        for str in hexdump_array:
            print(str)
        print()
        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50)
        for str in hexdump_array:
            print(str)
        print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
