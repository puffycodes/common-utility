# file: multi_level_index.py

import sys

class MultiLevelIndex:

    def __init__(self, max_level=2, empty_subkey='none'):
        if max_level <= 0:
            raise ValueError(f'max_level cannot be zero or less ({max_level})')
        self.data = {}
        self.max_level = max_level
        self.empty_subkey = empty_subkey
        return
    
    # --- Subkey Function
    
    def subkey(self, key, level):
        subkey = self.empty_subkey
        if len(key) > level:
            subkey = key[level]
        return subkey
    
    # --- External Interface
    
    def add(self, key, item):
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.get_container(curr_data, curr_subkey)
        self.add_item(curr_data, key, item)
        return
    
    def remove(self, key, item):
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.check_container(curr_data, curr_subkey)
            if curr_data == None:
                return
            if 'data' in curr_data:
                data_list = curr_data['data']
                if key in data_list:
                    if item in data_list[key]:
                        data_list[key].remove(item)
        return
    
    # TODO: Do not need this as we can use find_all()?
    def find_one(self, key):
        print(f'please use find_all({key})')
        return
    
    def find_all(self, key):
        result = []
        curr_data = self.data
        for i in range(self.max_level):
            curr_subkey = self.subkey(key, i)
            curr_data = self.check_container(curr_data, curr_subkey)
            if curr_data == None:
                return []
        if 'data' in curr_data:
            data_list = curr_data['data']
            if key in data_list:
                result = data_list[key]
        return result
    
    # --- Iterate through all the data
    
    def iterate_entry(self):
        level = 0
        for key, value in self.data.items():
            for key_n, value_n in self.iterate_entry_2(key, value, level):
                yield key_n, value_n
        return
    
    def iterate_entry_2(self, key, value, level):
        if level >= self.max_level:
            if key == 'data':
                for key_n, value_n in value.items():
                    yield (key_n, value_n)
        else:
            for key_n, value_n in value.items():
                for key_nn, value_nn in self.iterate_entry_2(key_n, value_n, level+1):
                    yield (key_nn, value_nn)
        return
    
    # --- Print the internal data structure
    
    def print(self, indent_char='-', fout=sys.stdout):
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
        if 'data' not in data:
            data['data'] = {}
        if key not in data['data']:
            data['data'][key] = []
        data['data'][key].append(item)
        return

# --- end of file --- #
