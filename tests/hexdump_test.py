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
    
    def test_hexdump(self):
        print()

        all_bytes = bytes([v for v in range(256)])
        
        hexdump_array = HexDump.hexdump(all_bytes)
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000000: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  |................|'
        )

        hexdump_array = HexDump.hexdump(all_bytes, bytes_per_line=32)
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000000: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F  |................................|'
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, sep='-')
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000030:       32-33-34-35-36-37-38-39-3A-3B-3C-3D-3E-3F  |  23456789:;<=>?|'
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='..')
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000050:                                         5A..5B..5C..5D..5E..5F  |          Z[\\]^_|'
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='')
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000050:                     5A5B5C5D5E5F  |          Z[\\]^_|'
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50,
                                        pos_label=0xff55)
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '0000ff50:                32 33 34 35 36 37 38 39 3A 3B 3C  |     23456789:;<|'
        )

        hexdump_array = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11
        )
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '0000bee9:                   32 33 34 35 36  |      23456|'
        )

        hexdump_array = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11, align_front=False
        )
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '0000beef: 32 33 34 35 36 37 38 39 3A 3B 3C  |23456789:;<|'
        )

        hexdump_array = HexDump.hexdump(all_bytes[10:-10])
        HexDump.print_hexdump(hexdump_array)
        self.assertEqual(
            hexdump_array[0],
            '00000000: 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19  |................|'
        )

        return
    
    def test_hexdump_start_and_end(self):
        verbose = True
        if verbose:
            print()
        data = bytes([v for v in range(65)])

        hexdump_array = HexDump.hexdump_start_and_end(data)
        if verbose:
            HexDump.print_hexdump(hexdump_array)
        self.assertEqual(len(hexdump_array), 5)

        # [ <byte_count_start>, <byte_count_end>, <expected_line_count> ]
        test_cases = [
            [ 16, 16, 4 ], [ 32, 32, 6 ], [ 33, 32, 5 ], [ 33, 31, 7 ],
        ]
        for start, end, expected_count in test_cases:
            hexdump_array = HexDump.hexdump_start_and_end(
                data, byte_count_start=start, byte_count_end=end
            )
            if verbose:
                data_length = len(data)
                print(f'data length: {data_length} = 0x{data_length:x}')
                print(f'start: {start}; end: {end}; expected line: {expected_count}')
                HexDump.print_hexdump(hexdump_array)
            self.assertEqual(len(hexdump_array), expected_count)

        for start, end, expected_count in test_cases:
            hexdump_array = HexDump.hexdump_start_and_end(
                data, byte_count_start=start, byte_count_end=end,
                pos_label=0xbeef
            )
            if verbose:
                data_length = len(data)
                print(f'data length: {data_length} = 0x{data_length:x}')
                print(f'start: {start}; end: {end}; expected line: {expected_count}')
                HexDump.print_hexdump(hexdump_array)
            # TODO: add checks
            # self.assertEqual(len(hexdump_array), expected_count_2)

        return
    
    def test_brief_hexdump(self):
        verbose = False

        if verbose:
            print()

        all_bytes = bytes([v for v in range(256)])

        hexdump_array = HexDump.hexdump(all_bytes)
        self.assertEqual(len(hexdump_array), 16)

        brief_hexdump_array = HexDump.brief_hexdump(hexdump_array)
        self.assertEqual(len(brief_hexdump_array), 16)

        # [ <start_line>, <end_line>, <expected_count> ]
        test_cases = [
            [ -1, -1, 16 ], [ -1, 0, 16 ], [ 0, -1, 16 ], [ 0, 0, 16 ],
            [ -1, 1, 2 ], [ 1, -1, 2 ], [ -1, 5, 6 ], [ 6, -1, 7 ],
            [ 1, 1, 3 ], [ 2, 1, 4 ], [ 5, 0, 6 ], [ 0, 6, 7 ],
            [ 3, 3, 7 ], [ 5, 3, 9 ], [ 5, 5, 11 ], [ 8, 7, 16 ],
            [ 8, 8, 16 ], [ 9, 9, 16 ], [ 16, 0, 16 ], [ 0, 16, 16 ],
            [ 17, 0, 16 ], [ 255, 0, 16 ], [ 0, 255, 16 ], [ 256, 256, 16 ],
        ]
        for start_line, end_line, expected_count in test_cases:
            brief_hexdump_array = HexDump.brief_hexdump(
                hexdump_array, start_line=start_line, end_line=end_line
            )
            if verbose:
                print(f'start_line: {start_line}; end_line: {end_line}; expected_count: {expected_count}')
                HexDump.print_hexdump(brief_hexdump_array, prefix='  ')
            self.assertEqual(len(brief_hexdump_array), expected_count)

        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
