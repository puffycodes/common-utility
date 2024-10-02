# file: hexdump_test.py

import unittest
import random
from common_util.hexdump import HexDump

class HexDumpTest(unittest.TestCase):

    def not_test_python_index_position(self):
        data = bytes([v for v in range(10)])
        data_length = len(data)
        print(f'length: {data_length}')
        for i in range(-12, 15):
            try:
                value = data[i]
                if i < 0:
                    value_2 = data[i+data_length]
                    equality = '==' if (value == value_2) else '!='
                    print(f'{i}: {value} {equality} {value_2}')
                else:
                    print(f'{i}: {value}')
            except Exception as e:
                print(f'{i}: {e}')
        return

    def test_to_hex_and_oct(self):
        data = bytes([ 0, 1, 2, 3, 4, 5, 32, 33, 34 ])
        # [ <array>, <kwargs>, <to_hex_result>, <to_oct_result> ]
        test_cases = [
            [ data, {}, '00 01 02 03 04 05 20 21 22', '000 001 002 003 004 005 040 041 042' ],
            [ data, { 'offset': 4 }, '04 05 20 21 22', '004 005 040 041 042' ],
            [ data, { 'length': 5 }, '00 01 02 03 04', '000 001 002 003 004' ],
            [ data, { 'pos': 2 }, '02 03 04 05 20 21 22', '002 003 004 005 040 041 042' ],
            [ data, { 'offset': 4, 'length': 3 }, '04 05 20', '004 005 040' ],
            [ data, { 'offset': 4, 'pos': 2 }, '20 21 22', '040 041 042' ],
            [ data, { 'offset': 4, 'length': 2, 'pos': 2 }, '20 21', '040 041' ],
            [ data, { 'offset': 4, 'length': 2, 'pos': 3 }, '21 22', '041 042' ],
            [ data, { 'offset': 4, 'length': 2, 'pos': 4 }, '22', '042' ],
            [ data, { 'offset': 4, 'length': 2, 'pos': 5 }, '', '' ],
            [ data, { 'length': 5, 'sep': '/' }, '00/01/02/03/04', '000/001/002/003/004' ],
            [ data, { 'length': 5, 'sep': '..'}, '00..01..02..03..04', '000..001..002..003..004' ],
            [ data, { 'length': 5, 'sep': ''}, '0001020304', '000001002003004' ],

            [ data[2:5], {}, '02 03 04', '002 003 004' ],
            [ data[2:5], { 'pos': 1 }, '03 04', '003 004' ],
            [ data[2:5], { 'pos': 5 }, '', '' ],

            # Negative start position
            [ data, { 'offset': -5 }, '04 05 20 21 22', '004 005 040 041 042' ],
            [ data, { 'pos': -5 }, '04 05 20 21 22', '004 005 040 041 042' ],
            [ data, { 'offset': -5, 'pos': -5 }, '22', '042' ],
            [ data, { 'offset': -5, 'length': 5, 'pos': -5 }, '22', '042' ],
            [ data, { 'offset': -5, 'length': -5, 'pos': -5 }, '22', '042' ],
            [ data, { 'offset': -5, 'length': 5, 'pos': -6 }, '21 22', '041 042' ],

            [ data[2:5], { 'pos': -5 }, '03 04', '003 004' ],
            [ data[2:5], { 'offset': 2, 'pos': -5 }, '02 03 04', '002 003 004' ],
            [ data[2:5], { 'offset': 5, 'pos': -5 }, '02 03 04', '002 003 004' ],
            [ data[2:5], { 'offset': 6, 'pos': -5 }, '03 04', '003 004' ],
        ]
        for array, kwargs, to_hex_result, to_oct_result in test_cases:
            self.assertEqual(HexDump.to_hex(array, **kwargs), to_hex_result)
            self.assertEqual(HexDump.to_oct(array, **kwargs), to_oct_result)
        return

    def test_to_text(self):
        data = bytes([ 0, 1 ])
        data += b'abcdefg'
        # [ <array>, <kwargs>, <to_text_result> ]
        test_cases = [
            [ data, {}, '..abcdefg' ],
            [ data, { 'offset': 4 }, 'cdefg' ],
            [ data, { 'length': 3 }, '..a' ],
            [ data, { 'pos': 5 }, 'defg' ],
            [ data, { 'offset': 4, 'length': 3, 'pos': 2 }, 'efg' ],
            [ data, { 'offset': 4, 'length': 3, 'pos': 3 }, 'fg' ],
            [ data, { 'offset': 4, 'length': 3, 'pos': 4 }, 'g' ],
            [ data, { 'offset': 4, 'length': 3, 'pos': 5 }, '' ],
            [ data, { 'offset': -4, 'length': 3, 'pos': 0 }, 'def' ],
            [ data, { 'offset': -4, 'length': 4, 'pos': 0 }, 'defg' ],
            [ data, { 'offset': -4, 'length': 5, 'pos': 0 }, 'defg' ],
        ]
        for array, kwargs, to_text_result in test_cases:
            self.assertEqual(HexDump.to_text(array, **kwargs), to_text_result)
        return
    
    def test_to_hex_array(self):
        data = bytes([ 0, 1 ])
        data += b'abcdefg'
        test_cases = [
            [ HexDump.to_hex_array(data), [ '00', '01', '61', '62', '63', '64', '65', '66', '67' ] ],
            [ HexDump.to_hex_array(data, offset=4), [ '63', '64', '65', '66', '67' ] ],
        ]
        for result, expected_result in test_cases:
            self.assertEqual(result, expected_result)
        return

    def test_to_oct_array(self):
        data = bytes([ 0, 1 ])
        data += b'abcdefg'
        test_cases = [
            [ HexDump.to_oct_array(data), [ '000', '001', '141', '142', '143', '144', '145', '146', '147' ] ],
            [ HexDump.to_oct_array(data, offset=4), [ '143', '144', '145', '146', '147' ] ],
        ]
        for result, expected_result in test_cases:
            self.assertEqual(result, expected_result)
        return
    
    def test_hex_array_to_string(self):
        data = [ '63', '65', 'FF' ]
        data_2 = [ '  ', '  ' ]
        data_2.extend(data)
        data_2.extend([ '  ' ])
        data_empty = []

        test_cases = [
            [ HexDump.hex_array_to_string(data), '63 65 FF' ],
            [ HexDump.hex_array_to_string(data_2), '      63 65 FF   ' ],
            [ HexDump.hex_array_to_string(data_empty), '' ],
            [ HexDump.hex_array_to_string(data[0:1]), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1]), '  ' ],

            [ HexDump.hex_array_to_string(data, sep=''), '6365FF' ],
            [ HexDump.hex_array_to_string(data_2, sep=''), '    6365FF  ' ],
            [ HexDump.hex_array_to_string(data_empty, sep=''), '' ],
            [ HexDump.hex_array_to_string(data[0:1], sep=''), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1], sep=''), '  ' ],

            [ HexDump.hex_array_to_string(data, sep='='), '63=65=FF' ],
            [ HexDump.hex_array_to_string(data_2, sep='='), '      63=65=FF   ' ],
            [ HexDump.hex_array_to_string(data_empty, sep='='), '' ],
            [ HexDump.hex_array_to_string(data[0:1], sep='='), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1], sep='='), '  ' ],

            [ HexDump.hex_array_to_string(data, sep='=='), '63==65==FF' ],
            [ HexDump.hex_array_to_string(data_2, sep='=='), '        63==65==FF    ' ],
            [ HexDump.hex_array_to_string(data_empty, sep='=='), '' ],
            [ HexDump.hex_array_to_string(data[0:1], sep='=='), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1], sep='=='), '  ' ],

            [ HexDump.hex_array_to_string(data, sep='  '), '63  65  FF' ],
            [ HexDump.hex_array_to_string(data_2, sep='  '), '        63  65  FF    ' ],
            [ HexDump.hex_array_to_string(data_empty, sep='  '), '' ],
            [ HexDump.hex_array_to_string(data[0:1], sep='  '), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1], sep='  '), '  ' ],

            [ HexDump.hex_array_to_string(data, sep=' .'), '63 .65 .FF' ],
            [ HexDump.hex_array_to_string(data_2, sep=' .'), '        63 .65 .FF    ' ],
            [ HexDump.hex_array_to_string(data_empty, sep=' .'), '' ],
            [ HexDump.hex_array_to_string(data[0:1], sep=' .'), '63' ],
            [ HexDump.hex_array_to_string(data_2[0:1], sep=' .'), '  ' ],
        ]

        for result, expected_result in test_cases:
            self.assertEqual(result, expected_result)
        return
    
    def test_oct_array_to_string(self):
        data = [ '000', '   ', '001', '002', '003', '   ', '004', '   ', '   ', '   ' ]
        test_cases = [
            [
                HexDump.hex_array_to_string(data),
                '000     001 002 003     004            '
            ],
            [
                HexDump.hex_array_to_string(data, sep=''),
                '000   001002003   004         '
            ],
            [
                HexDump.hex_array_to_string(data, sep='-'),
                '000     001-002-003     004            '
            ],
            [
                HexDump.hex_array_to_string(data, sep='=='),
                '000       001==002==003       004               '
            ],
            [
                HexDump.hex_array_to_string(data, sep='  '),
                '000       001  002  003       004               '
            ],
            [
                HexDump.hex_array_to_string(data, sep=' .'),
                '000       001 .002 .003       004               '
            ],
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
        verbose = True
        kwargs_octal = { 'dump_type': HexDump.DUMPTYPE_OCT }

        all_bytes = bytes([v for v in range(256)])

        print()
        
        hexdump_array = HexDump.hexdump(all_bytes)
        hexdump_array_octal = HexDump.hexdump(all_bytes, **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000000: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  |................|',
            '00000000: 000 001 002 003 004 005 006 007 010 011 012 013 014 015 016 017  |................|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes, bytes_per_line=32)
        hexdump_array_octal = HexDump.hexdump(all_bytes, bytes_per_line=32, **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000000: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F  |................................|',
            '00000000: 000 001 002 003 004 005 006 007 010 011 012 013 014 015 016 017 020 021 022 023 024 025 026 027 030 031 032 033 034 035 036 037  |................................|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, sep='-')
        hexdump_array_octal = HexDump.hexdump(all_bytes, offset=50, length=50, sep='-',
                                              **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000030:       32-33-34-35-36-37-38-39-3A-3B-3C-3D-3E-3F  |  23456789:;<=>?|',
            '00000030:         062-063-064-065-066-067-070-071-072-073-074-075-076-077  |  23456789:;<=>?|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='..')
        hexdump_array_octal = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                              sep='..', **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000050:                                         5A..5B..5C..5D..5E..5F  |          Z[\\]^_|',
            '00000050:                                                   132..133..134..135..136..137  |          Z[\\]^_|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                        sep='')
        hexdump_array_octal = HexDump.hexdump(all_bytes, offset=50, length=50, pos=40,
                                              sep='', **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000050:                     5A5B5C5D5E5F  |          Z[\\]^_|',
            '00000050:                               132133134135136137  |          Z[\\]^_|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes, offset=50, length=50,
                                        pos_label=0xff55)
        hexdump_array_octal = HexDump.hexdump(all_bytes, offset=50, length=50,
                                              pos_label=0xff55, **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '0000ff50:                32 33 34 35 36 37 38 39 3A 3B 3C  |     23456789:;<|',
            '0000ff50:                     062 063 064 065 066 067 070 071 072 073 074  |     23456789:;<|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11
        )
        hexdump_array_octal = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11,
            **kwargs_octal
        )
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '0000bee9:                   32 33 34 35 36  |      23456|',
            '0000bee9:                         062 063 064 065 066  |      23456|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11, align_front=False
        )
        hexdump_array_octal = HexDump.hexdump(
            all_bytes, offset=50, length=50, pos_label=0xbeef, bytes_per_line=11, align_front=False,
            **kwargs_octal
        )
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '0000beef: 32 33 34 35 36 37 38 39 3A 3B 3C  |23456789:;<|',
            '0000beef: 062 063 064 065 066 067 070 071 072 073 074  |23456789:;<|',
            verbose=verbose
        )

        hexdump_array = HexDump.hexdump(all_bytes[10:-10])
        hexdump_array_octal = HexDump.hexdump(all_bytes[10:-10], **kwargs_octal)
        self.do_check_hexdump(
            hexdump_array, hexdump_array_octal,
            '00000000: 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 16 17 18 19  |................|',
            '00000000: 012 013 014 015 016 017 020 021 022 023 024 025 026 027 030 031  |................|',
            verbose=verbose
        )

        return
    
    def do_check_hexdump(self, hexdump_array, hexdump_array_oct,
                         expected_result_01, expected_result_02,
                         verbose=False):
        if verbose:
            print(f'---')
            print(f'Hexadecimal:')
            HexDump.print_hexdump(hexdump_array)
            print()
            print(f'Octal:')
            HexDump.print_hexdump(hexdump_array_oct)
            print()
        self.assertEqual(hexdump_array[0], expected_result_01)
        self.assertEqual(hexdump_array_oct[0], expected_result_02)
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

        # [ <byte_count_start>, <byte_count_end>, <expected_line_count_1>, <expected_line_count_2> ]
        test_cases = [
            [ 16, 16, 4, 4 ], [ 32, 32, 6, 6 ], [ 33, 32, 5, 5 ], [ 33, 31, 7, 6 ],
            [ 0, 64, 6, 5 ], [ 64, 0, 5, 6 ], [ 0, 63, 6, 5 ], [ 63, 0, 5, 6 ],
        ]
        for start, end, expected_count_1, _ in test_cases:
            hexdump_array = HexDump.hexdump_start_and_end(
                data, byte_count_start=start, byte_count_end=end
            )
            if verbose:
                data_length = len(data)
                print(f'data length: {data_length} = 0x{data_length:x}')
                print(f'start: {start}; end: {end}; expected line: {expected_count_1}')
                HexDump.print_hexdump(hexdump_array)
                print()
            self.assertEqual(len(hexdump_array), expected_count_1)

        for start, end, _, expected_count_2 in test_cases:
            hexdump_array = HexDump.hexdump_start_and_end(
                data, byte_count_start=start, byte_count_end=end,
                pos_label=0xbeef
            )
            if verbose:
                data_length = len(data)
                print(f'data length: {data_length} = 0x{data_length:x}')
                print(f'start: {start}; end: {end}; expected line: {expected_count_2}')
                HexDump.print_hexdump(hexdump_array)
                print()
            self.assertEqual(len(hexdump_array), expected_count_2)

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
                print()
            self.assertEqual(len(brief_hexdump_array), expected_count)

        return
    
    def test_hexdump_and_print(self):
        data = [_ % 256 for _ in range(10000)]
        pos_label_list = [ 0, 33, 679, 500, 9998 ]
        data_list = [ data[pos:pos+random.randint(31,68)] for pos in pos_label_list ]
        label_list = [ f'data at position {pos} (0x{pos:x}):' for pos in pos_label_list ]
        kwargs_list = [
            { }, { 'dump_type': HexDump.DUMPTYPE_OCT },
        ]
        for kwargs in kwargs_list:
            print()
            print(f'=== test hexdump_and_print() ===')
            HexDump.hexdump_and_print(
                data_list, label_list=label_list, pos_label_list=pos_label_list,
                max_bytes_show=48, **kwargs
            )
            print(f'=== test end hexdump_and_print() ===')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
