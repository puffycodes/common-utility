# file: hexdump_test.py

import unittest
from common_util.hexdump import HexDump

class HexDumpTest(unittest.TestCase):

    def test_to_hex(self):
        data = bytes([ 0, 1, 2, 3, 4, 5, 32, 33, 34 ])
        test_cases = [
            [ HexDump.to_hex(data), '00 01 02 03 04 05 20 21 22' ],
            [ HexDump.to_hex(data, offset=4), '04 05 20 21 22'],
            [ HexDump.to_hex(data, length=5), '00 01 02 03 04' ],
            [ HexDump.to_hex(data, pos=2), '02 03 04 05 20 21 22' ],
            [ HexDump.to_hex(data, offset=4, length=3), '04 05 20'],
            [ HexDump.to_hex(data, offset=4, pos=2), '20 21 22' ],
            [ HexDump.to_hex(data, offset=4, length=2, pos=2), '20 21'],
            [ HexDump.to_hex(data, offset=4, length=2, pos=3), '21 22'],
            [ HexDump.to_hex(data, offset=4, length=2, pos=4), '22'],
            [ HexDump.to_hex(data, length=5, sep='/'), '00/01/02/03/04' ],
            [ HexDump.to_hex(data, length=5, sep='..'), '00..01..02..03..04' ],
            [ HexDump.to_hex(data, length=5, sep=''), '0001020304' ],
            [ HexDump.to_hex(data[2:5]), '02 03 04' ],
        ]
        for result, expected_result in test_cases:
            self.assertEqual(result, expected_result)
        return
    
    def test_to_text(self):
        data = bytes([ 0, 1 ])
        data += b'abcdefg'
        test_cases = [
            [ HexDump.to_text(data), '..abcdefg' ],
            [ HexDump.to_text(data, offset=4), 'cdefg' ],
            [ HexDump.to_text(data, length=3), '..a' ],
            [ HexDump.to_text(data, pos=5), 'defg' ],
            [ HexDump.to_text(data, offset=4, length=3, pos=2), 'efg' ],
            [ HexDump.to_text(data, offset=4, length=3, pos=3), 'fg' ],
            [ HexDump.to_text(data, offset=4, length=3, pos=4), 'g' ],
            [ HexDump.to_text(data, offset=4, length=3, pos=5), '' ],
        ]
        for result, expected_result in test_cases:
            self.assertEqual(result, expected_result)
        return

    def test_01(self):
        all_bytes = bytes([v for v in range(256)])
        print()
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
        print()
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
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11
        )
        HexDump.print_hexdump(hexdump_array)

        hexdump_array = HexDump.hexdump(all_bytes[10:-10])
        HexDump.print_hexdump(hexdump_array)

        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
