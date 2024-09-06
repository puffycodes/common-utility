# file: multi_level_index_test.py

import unittest
import sys
from common_util.container.multi_level_index import MultiLevelIndex

class SubkeyGeneratorTest(unittest.TestCase):

    def test_subkey_using_hash(self):
        key_gen_list = [
            MultiLevelIndex.SubkeyGeneratorUsingHash(),
            MultiLevelIndex.SubkeyGeneratorUsingHash(empty_subkey='empty')
        ]
        test_keys = [
            'abcdef', 'abcdefghijklmnopqrstuvwxyz',
        ]
        for key_gen in key_gen_list:
            for key in test_keys:
                for i in range(10):
                    subkey = key_gen.get_subkey(key, i)
                    if i < len(key):
                        self.assertEqual(subkey, key[i])
                    else:
                        self.assertEqual(subkey, key_gen.get_empty_subkey())
                for i in range(-10, 0):
                    with self.assertRaises(ValueError):
                        subkey = key_gen.get_subkey(key, i)
        return

class MultiLevelIndexTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        return

    def test_subkey(self):
        self.sd = MultiLevelIndex()
        key = 'abcdefg'
        for i in range(10):
            print(self.sd.subkey(key, i), end=' ')
        print()
        return
    
    def test_add(self):
        search_items = ['abc', 'za', 'abcgg', 'a', 'z']

        self.sd1 = MultiLevelIndex()
        self.do_add(self.sd1)
        self.do_print_and_find(self.sd1, search_items)

        self.sd2 = MultiLevelIndex(max_level=3)
        self.do_add(self.sd2)
        self.do_print_and_find(self.sd2, search_items)

        print(f'-***')
        self.do_iterate_entry(self.sd1)
        print()
        print(f'-***')
        self.do_iterate_entry(self.sd2)
        print()
        return
    
    def do_add(self, sd):
        sd.add('abc', (1, 1))
        sd.add('abd', (1, 2))
        sd.add('adcb', (1, 3))
        sd.add('acdbe', (1, 4))
        sd.add('a', (1, 5))
        sd.add('abcd', (1, 6))
        sd.add('bc', (2, 1))
        sd.add('bcd', (2, 2))
        sd.add('za', (4, 5))
        sd.add('abc', (20, 20))
        sd.add('abc', (20, 21))
        sd.add('abcdefghijkl', (30, 30))
        sd.add('aaa', (31, 31))
        sd.add('0abef', (101, 101))
        sd.remove('0abef', (100, 100))
        sd.add('gghh', (1, 1))
        sd.add('gghh', (2, 2))
        sd.add('gghh', (2, 3))
        sd.add('gghh', 'the quick brown fox')
        sd.remove('gghh', (2, 2))
        return
    
    def do_print_and_find(self, sd, keys):
        sd.print(fout=sys.stdout)
        print(f'-----***-----')
        for key in keys:
            print(f'- {key}: {sd.find_all(key)}')
        print(f'=====***=====')
        print()
        return
    
    def do_iterate_entry(self, sd):
        for key, value in sd.iterate_entry():
            print(f'- {key}: {value}')
        return
    
    def test_error(self):
        with self.assertRaises(ValueError):
            sd_error = MultiLevelIndex(max_level=0)
        with self.assertRaises(ValueError):
            sd_error = MultiLevelIndex(max_level=-1)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
