# file: multi_level_index.py

'''
Containers of items
'''

import sys

class MultiLevelIndex:
    '''
    A containers that stored items by buckets indexed by subkey.
    The subkeys are derived from a main key.
    '''

    # - Subkey Generator Classes

    class SubkeyGenerator:
        '''
        An abstract class for subkey generation.
        '''

        def __init__(self, empty_subkey='none'):
            self.empty_subkey = empty_subkey
            return
        
        def get_subkey(self, key, level):
            '''
            Get the subkey from key at the desired level

            This function needs to be implemented in sub-classes.

            :param key: the key
            :param level: the level of the subkey
            :type key: str
            :type level: int

            :return: subkey
            :rtype: str
            '''
            raise Exception('get_subkey() must be implemented in sub-class.')
        
        def check_level(self, key, level):
            '''
            Check that the level is valid for the key

            :param key: the key
            :param level: the level of the subkey
            :type key: str
            :type level: int

            :return: level
            :rtype: int
            '''
            if level < 0:
                raise ValueError(f'level cannot be negative ({level})')
            return level

        def get_empty_subkey(self):
            '''
            Return the str that is the empty subkey

            :return: empty subkey
            :rtype: str
            '''
            return self.empty_subkey
        
        def get_subkey_from_string(self, string, level):
            '''
            Returns the level'th charactor of the string as subkey

            This function can be used by the sub-classes

            :param string: the string from which the subkey is derived
            :param level: the level of the subkey
            :type string: str
            :type level: int

            :return: subkey
            :rtype: str
            '''
            subkey = self.empty_subkey
            if len(string) > level:
                subkey = string[level]
            return subkey
        
    class SubkeyGeneratorUsingHash(SubkeyGenerator):
        '''
        A subkey generator that returns the nth charactor of the key as the subkey.
        Suitable for keys such as a hash digest.
        '''

        def __init__(self, empty_subkey='none'):
            super().__init__(empty_subkey=empty_subkey)
            return
        
        def get_subkey(self, key, level):
            '''
            Get the subkey from key at the desired level

            :param key: the key
            :param level: the level of the subkey
            :type key: str
            :type level: int

            :return: subkey
            :rtype: str
            '''
            self.check_level(key, level)
            # subkey = self.empty_subkey
            # if len(key) > level:
            #     subkey = key[level]
            # return subkey
            return self.get_subkey_from_string(key, level)
        
    # - Multi-Level Index Class

    def __init__(self, max_level=2, key_generator=None):
        '''
        Initialize the object

        :param max_level: the maximum level of subkey
        :param key_generator: a key generator of the class SubkeyGenerator
        :type max_level: int, optional
        :type key_generator: sub-class of SubkeyGenerator, optional

        :return: no value is returned by this function
        '''
        if max_level <= 0:
            raise ValueError(f'max_level cannot be zero or less ({max_level})')
        self.data = {}
        self.max_level = max_level
        if key_generator == None:
            self.key_generator = MultiLevelIndex.SubkeyGeneratorUsingHash(
                empty_subkey='none'
            )
        else:
            self.key_generator = key_generator
        self.data_container_tag = 'data'
        return
    
    # --- Subkey Function
    
    def subkey(self, key, level):
        '''
        Obtain the subkey from key and level

        :meta private:
        :param key: the key
        :param level: the desired level
        :type key: str
        :type level: int

        :return: the subkey
        :rtype: str
        '''
        return self.key_generator.get_subkey(key, level)
    
    # --- External Interface
    
    def add(self, key, item):
        '''
        Add an item to the Index with key

        :param key: the key
        :param item: the item
        :type key: str
        :type item: any object

        :return: nothing returned
        '''
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.get_container(curr_data, curr_subkey)
        self.add_item(curr_data, key, item)
        return
    
    def remove(self, key, item):
        '''
        Remove an item from the Index with key, if present

        :param key: the key
        :param item: the item
        :type key: str
        :type item: any object

        :return: nothing returned
        '''
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.check_container(curr_data, curr_subkey)
            if curr_data == None:
                return
            if self.data_container_tag in curr_data:
                data_list = curr_data[self.data_container_tag]
                if key in data_list:
                    if item in data_list[key]:
                        data_list[key].remove(item)
        return
    
    # TODO: Do not need this as we can use find_all()?
    def find_one(self, key):
        print(f'please use find_all({key})')
        return
    
    def find_all(self, key):
        '''
        Find all object that has the key

        :param key: the key
        :type key: str

        :return: the list of items with key
        :rtype: list of item
        '''
        result = []
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.check_container(curr_data, curr_subkey)
            if curr_data == None:
                return []
        if self.data_container_tag in curr_data:
            data_list = curr_data[self.data_container_tag]
            if key in data_list:
                result = data_list[key]
        return result
    
    # --- Iterate through all the data
    
    def iterate_entry(self):
        '''
        Iterate through all the entries in the Index

        :meta privae:
        :return: (key, value), where key is the key, and value the object
        :rtype: tuple
        '''
        level = 0
        for key, value in self.data.items():
            for key_n, value_n in self.iterate_entry_2(key, value, level):
                yield key_n, value_n
        return
    
    def iterate_entry_2(self, key, value, level):
        if level >= self.max_level:
            if key == self.data_container_tag:
                for key_n, value_n in value.items():
                    yield (key_n, value_n)
        else:
            for key_n, value_n in value.items():
                for key_nn, value_nn in self.iterate_entry_2(key_n, value_n, level+1):
                    yield (key_nn, value_nn)
        return
    
    # --- Print the internal data structure
    
    def print(self, indent_char='-', fout=sys.stdout):
        '''
        Print the internal representation of the index

        :param indent_char: the character to used for indentation
        :param fout: file id to output the index
        :type indent_char: str, optional
        :type fout: file id, optional
        '''
        level = 0
        for key, value in self.data.items():
            self.print_2(key, value, level, indent_char=indent_char, fout=fout)
        return
    
    def print_2(self, key, value, level, indent_char='-', fout=sys.stdout):
        if level > self.max_level:
            print(f'{indent_char*level}{key}: {value}', file=fout)
        else:
            print(f'{indent_char*level}{key}:', file=fout)
            for key_n, value_n in value.items():
                self.print_2(key_n, value_n, level+1, fout=fout)
        return
    
    # --- Internal Functions
    
    def check_container(self, data, subkey):
        result = None
        if subkey in data:
            result = data[subkey]
        return result
        
    def get_container(self, data, subkey):
        if subkey not in data:
            data[subkey] = {}
        return data[subkey]
    
    def add_item(self, data, key, item):
        if self.data_container_tag not in data:
            data[self.data_container_tag] = {}
        if key not in data[self.data_container_tag]:
            data[self.data_container_tag][key] = []
        data[self.data_container_tag][key].append(item)
        return

# --- end of file --- #
