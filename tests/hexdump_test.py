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
        print(f'-- {HexDump.to_hex(all_bytes, length=50, sep="/")}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50, sep="..")}')
        print(f'-- {HexDump.to_hex(all_bytes, length=50, sep="")}')
        print()
        print(f'-- {HexDump.to_text(all_bytes)}')
        print(f'-- {HexDump.to_text(all_bytes, offset=32)}')
        print(f'-- {HexDump.to_text(all_bytes, offset=32, length=20)}')
        return
    
    def test_02(self):
        print()

        all_bytes = bytes([v for v in range(256)])
        
        hexdump_array = HexDump.hexdump(all_bytes)
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes, bytes_per_line=32)
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, sep='-')
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='..')
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='')
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50,
                                        pos_label=0xff55)
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0x55, bytes_per_line=11
        )
        HexDump.print_hexdump(hexdump_array)

        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
