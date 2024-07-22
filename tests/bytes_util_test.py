# file: bytes_util_test.py

from threading import excepthook
import unittest
from common_util.bytes_util import BytesUtility

class BytesUtilityTest(unittest.TestCase):
    def test_xor(self):
        a = b'abcde'
        b = b'abcdefg'
        r1 = b'\x00\x00\x00\x00\x00'
        r2 = b'\x00\x00\x00\x00\x00fg'
        self.assertEqual(BytesUtility.xor(a, b), r1)
        self.assertEqual(BytesUtility.xor(a, b, trancate=True), r1)
        self.assertEqual(BytesUtility.xor(a, b, trancate=False), r2)
        self.assertEqual(BytesUtility.xor(b, a), r1)
        self.assertEqual(BytesUtility.xor(b, a, trancate=True), r1)
        self.assertEqual(BytesUtility.xor(b, a, trancate=False), r2)
        return
    
    def test_integer_to_bytes_01(self):
        test_values = [ 0, 5, 65535, 12345678901234567890 ]
        test_bytes_length = 20
        for value in test_values:
            bytes_value = BytesUtility.integer_to_bytes(
                value, test_bytes_length
            )
            self.assertEqual(
                BytesUtility.has_sufficient_bytes(
                    bytes_value, 0, test_bytes_length
                ),
                True
            )
            new_value = BytesUtility.extract_integer(
                bytes_value, 0, test_bytes_length
            )
            self.assertEqual(new_value, value)
        return
    
    def test_integer_to_bytes_02(self):
        test_values = [ 0, 5, 65535, 280, 3456, 42 ]
        test_bytes_lengths = [ 2, 4, 8, 8, 16, 2 ]
        data = b''
        for value, length in zip(test_values, test_bytes_lengths):
            data += BytesUtility.integer_to_bytes(value, length)
        curr_pos = 0
        for value, length in zip(test_values, test_bytes_lengths):
            self.assertEqual(
                BytesUtility.has_sufficient_bytes(data, 0, length, pos=curr_pos),
                True
            )
            new_value = BytesUtility.extract_integer(data, 0, length, pos=curr_pos)
            self.assertEqual(new_value, value)
            curr_pos += length
        return
    
    def test_integer_to_bytes_03(self):
        # [ <data>, <little_endian_value>, <big_endian_value> ]
        test_dataset = [
            [ b'\x00\x01\x02\x03', 50462976, 66051 ],
            [ b'\x00\x01', 256, 1 ],
            [ b'\x00\x00\x01', 65536, 1 ],
        ]
        for data, expected_little, expected_big in test_dataset:
            value_default = BytesUtility.extract_integer(
                data, 0, len(data)
            )
            value_little = BytesUtility.extract_integer(
                data, 0, len(data), endian='little'
            )
            value_big = BytesUtility.extract_integer(
                data, 0, len(data), endian='big'
            )
            self.assertEqual(value_default, expected_little)
            self.assertEqual(value_little, expected_little)
            self.assertEqual(value_big, expected_big)
        return
    
    def test_bytes_rep_to_bytes_01(self):
        a = b'abcde'
        b = b'\x00\xab\r\n\tabcde\'\\'
        self.assertEqual(BytesUtility.bytes_rep_to_bytes(f'{a}'), a)
        self.assertEqual(BytesUtility.bytes_rep_to_bytes(f'{b}'), b)
        return
    
    def test_bytes_rep_to_bytes_02(self):
        test_rep_01 = "b'a\\r\\x01c'"
        test_rep_bytes_01 = b'a\r\x01c'
        self.assertEqual(
            BytesUtility.bytes_rep_to_bytes(test_rep_01), test_rep_bytes_01
        )
        test_rep_02 ="b'a\\z'"
        test_rep_bytes_02 = b'a***unknown(\\z)***'
        self.assertEqual(
            BytesUtility.bytes_rep_to_bytes(test_rep_02), test_rep_bytes_02
        )
        test_rep_03 = '%s' % (b'\n\t\r\b\f\"\'\0\1\01\013\xfe')
        test_rep_bytes_03 = b'\n\t\r\x08\x0c"\'\x00\x01\x01\x0b\xfe'
        self.assertEqual(
            BytesUtility.bytes_rep_to_bytes(test_rep_03), test_rep_bytes_03
        )
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
