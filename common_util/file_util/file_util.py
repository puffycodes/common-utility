# file: file_util.py

'''
Utilities for Files
'''

import os
import hashlib

class FileUtility:
    '''
    A collection of utilities for handling files
    '''

    @staticmethod
    def get_file_size(dirname, filename):
        '''
        Return the file size of a file

        :param dirname: the name of the directory
        :type dirname: str
        :param filename: the name of the file
        :type filename: str

        :return: the size of the file
        :rtype: int
        '''
        full_filename = os.path.join(dirname, filename)
        file_size = os.path.getsize(full_filename)
        return file_size

    @staticmethod
    def get_file_md5_hash(dirname, filename):
        '''
        Compute the MD5 digest of a file

        :param dirname: the name of the directory
        :type dirname: str
        :param filename: the name of the file
        :type filename: str

        :return: the MD5 digest of the file
        :rtype: str
        '''
        full_filename = os.path.join(dirname, filename)
        with open(full_filename, 'rb') as fd:
            data = fd.read()
        data_hash = hashlib.md5(data)
        digest = data_hash.hexdigest()
        return digest

# --- end of file --- #
