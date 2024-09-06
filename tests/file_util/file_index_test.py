# file: file_index_test.py

import unittest
from common_util.dir_util import DirectoryUtility
from common_util.file_util.file_index import FileIndex

class FileIndexKeyGeneratorTest(unittest.TestCase):

    def test_key_generator_using_filename(self):
        test_dir_list = [
            '.',
        ]
        key_gen_list = [
            FileIndex.SubkeyGeneratorUsingFilename(),
            FileIndex.SubkeyGeneratorUsingFilename(use_file_extension=False),
        ]
        for test_dir in test_dir_list:
            file_list = DirectoryUtility.list_files(test_dir, '*', recursive=True)
            for file in file_list:
                print(f'{file}:')
                for key_gen in key_gen_list:
                    subkey_list = []
                    for i in range(10):
                        subkey = key_gen.get_subkey(file, i)
                        subkey_list.append(subkey)
                    print(f'subkeys: {subkey_list}')
                print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
