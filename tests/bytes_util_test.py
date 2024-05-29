# file: bytes_util_test.py

import unittest
from common_util import bytes_util

class BytesUtilityTest(unittest.TestCase):
    def test_xor(self):
        a = b'abcde'
        b = b'abcdefg'
        r1 = b'\x00\x00\x00\x00\x00'
        r2 = b'\x00\x00\x00\x00\x00fg'
        self.assertEqual(bytes_util.BytesUtility.xor(a, b), r1)
        self.assertEqual(bytes_util.BytesUtility.xor(a, b, trancate=False), r2)
        self.assertEqual(bytes_util.BytesUtility.xor(b, a), r1)
        self.assertEqual(bytes_util.BytesUtility.xor(b, a, trancate=False), r2)
        return
    
    def test_bytes_rep_to_bytes(self):
        a = b'abcde'
        b = b'\x00\xab\r\n\tabcde\'\\'
        self.assertEqual(bytes_util.BytesUtility.bytes_rep_to_bytes(f'{a}'), a)
        self.assertEqual(bytes_util.BytesUtility.bytes_rep_to_bytes(f'{b}'), b)
        return
    
    def test_bytes_rep_to_bytes_02(self):
        test_rep_01 = "b'a\\r\\x01c'"
        test_rep_bytes_01 = b'a\r\x01c'
        self.assertEqual(
            bytes_util.BytesUtility.bytes_rep_to_bytes(test_rep_01), test_rep_bytes_01
        )
        test_rep_02 ="b'a\z'"
        test_rep_bytes_02 = b'a***unknown(\\z)***'
        self.assertEqual(
            bytes_util.BytesUtility.bytes_rep_to_bytes(test_rep_02), test_rep_bytes_02
        )
        test_rep_03 = '%s' % (b'\n\t\r\b\f\"\'\0\1\01\013\xfe')
        test_rep_bytes_03 = b'\n\t\r\x08\x0c"\'\x00\x01\x01\x0b\xfe'
        self.assertEqual(
            bytes_util.BytesUtility.bytes_rep_to_bytes(test_rep_03), test_rep_bytes_03
        )
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #