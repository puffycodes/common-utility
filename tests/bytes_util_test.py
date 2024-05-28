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

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #