# file: dir_util.py

'''
Utilities for Directory
'''

import os
import sys
import shutil
from glob import glob

class DirectoryUtility:
    '''
    A collection of utilities for handling directories
    '''

    # --- Exceptions defined in this module

    class SourceAndDestintionSame(Exception):
        '''
        Exception that is raised when the source and destination of a copy action
        are actually the same file/directory.
        '''
        pass

    class NotAFileError(Exception):
        '''
        Exception that is raised when the target is not a file (e.g. a directory)
        when it is expected to be one.
        '''
        pass

    class FileIsAbsolutePathError(Exception):
        '''
        Exception that is raised when a path is an absolute path when it is
        expected to be a relative path.
        '''
        pass

    class NotInBaseDirectory(Exception):
        '''
        Exception that is raised when a path is not within a certain base directory
        when it is expected to be.
        '''
        pass

    # --- Main API for this modules

    @staticmethod
    def list_files(dirname: str, filename_pattern: str,
                   recursive=False, include_hidden=False, get_relative_path=False,
                   verbose=False, ferr=sys.stderr):
        '''
        Obtain a list of files from a directory.

        :param dirname: the name of the directory
        :param filename_pattern: the pattern of the file names to include in the
            result
        :type dirname: str
        :type filename_pattern: str

        :param recursive: when True, do the listing recursively into subdirectories
        :param include_hidden: when True, include files that are normally considered
            hidden;
            this option works only for Python 3.11 and later
        :param get_relative_path: when True, return the file names as a path relative
            to dirname; when False, the file names will include dirname as a prefix
        :type recursive: bool, optional
        :type include_hidden: bool, optional
        :type get_relative_path: bool, optional

        :param verbose: when True, print some debugging information
        :param ferr: the file id to print the debugging information to; default is
            sys.stderr
        :type verbose: bool, optional
        :type ferr: file id, optional

        :return: a list of file names
        :rtype: list of str
        '''
        dirname_normalized = os.path.normpath(dirname)
        if verbose:
            print(f'given directory path is "{dirname}".', file=ferr)
            print(f'normalized directory path is "{dirname_normalized}".', file=ferr)

        file_list = []
        glob_kwargs = DirectoryUtility.get_glob_kwargs(include_hidden=include_hidden)
        if recursive:
            file_list = glob(
                os.path.join(dirname_normalized, '**', filename_pattern),
                recursive=True, **glob_kwargs
            )
        else:
            file_list = glob(
                os.path.join(dirname_normalized, filename_pattern),
                **glob_kwargs
            )

        file_list = [os.path.normpath(file) for file in file_list]
        file_list = [file for file in file_list if os.path.isfile(file)]
        
        # There is no path prefix if dirname is '.'
        if dirname_normalized != '.':
            file_list = [file for file in file_list \
                         if file.startswith(dirname_normalized)]
        if get_relative_path: # and dirname_normalized != '.':
            file_list = DirectoryUtility.get_relative_path_list(
                file_list, dirname_normalized, verbose=verbose, ferr=ferr
            )
            
        return file_list

    @staticmethod
    def list_subdirectories(dirname: str, subdir_pattern: str,
                            recursive=False, include_hidden=False, get_relative_path=False,
                            verbose=False, ferr=sys.stderr):
        '''
        Obtain a list of subdirectories from a directory.

        :param dirname: the name of the directory
        :param subdir_pattern: the pattern of the subdirectory names to include in the
            result
        :type dirname: str
        :type subdir_pattern: str

        :param recursive: when True, do the listing recursively into subdirectories
        :param include_hidden: when True, include subdirectories that are normally
            considered hidden;
            this option works only for Python 3.11 and later
        :param get_relative_path: when True, return the subdirectory names as a path relative
            to dirname; when False, the subdirectory names will include dirname as a prefix
        :type recursive: bool, optional
        :type include_hidden: bool, optional
        :type get_relative_path: bool, optional

        :param verbose: when True, print some debugging information
        :param ferr: the file id to print the debugging information to; default is
            sys.stderr
        :type verbose: bool, optional
        :type ferr: file id, optional

        :return: a list of subdirectory names
        :rtype: list of str
        '''
        dirname_normalized = os.path.normpath(dirname)
        if verbose:
            print(f'given directory path is "{dirname}".', file=ferr)
            print(f'normalized directory path is "{dirname_normalized}".', file=ferr)

        subdir_list = []
        glob_kwargs = DirectoryUtility.get_glob_kwargs(include_hidden=include_hidden)
        if recursive:
            subdir_list = glob(
                os.path.join(dirname_normalized, '**', subdir_pattern),
                recursive=True, **glob_kwargs
            )
        else:
            subdir_list = glob(
                os.path.join(dirname_normalized, subdir_pattern),
                **glob_kwargs
            )

        subdir_list = [os.path.normpath(subdir) for subdir in subdir_list]
        subdir_list = [subdir for subdir in subdir_list if os.path.isdir(subdir)]

        # There is no path prefix if dirname is '.'
        if dirname_normalized != '.':
            subdir_list = [subdir for subdir in subdir_list \
                           if subdir.startswith(dirname_normalized)]
        if get_relative_path: # and dirname_normalized != '.':
            subdir_list = DirectoryUtility.get_relative_path_list(
                subdir_list, dirname_normalized, verbose=verbose, ferr=ferr
            )

        return subdir_list
    
    @staticmethod
    def copy_files(src_dir: str, dst_dir: str, filelist, verbose=False, ferr=sys.stderr):
        '''
        Copy a list of files from the source to the destination directory

        :param src_dir: source directory
        :param dst_dir: destination directory
        :param filelist: the list of files to copy;
            the file path should be relative to the source directory and within
            the source directory, otherwise it will not be copied
        :type src_dir: str
        :type dst_dir: str
        :type filelist: list of str

        :param verbose: when True, print some debugging information
        :param ferr: the file id to output the debugging information
        :type verbose: bool, optional
        :type ferr: file id, optional

        :return: (succeeded_file, failed_files) where the first is a list of
            successfully copied file, and the second is a list of files that
            failed to be copied;
            succeeded_file is a list of tuple (file, dst_file) where file is the
            given file name, and dst_file is the normalized destination file name
            relative to dst_dir;
            failed_files is a list of tuple (file, error) where file is the
            given file name, and error is the Exception for which the file failed
            to be copied
        :rtype: tuple
        '''
        # check that the source and destination are not the same
        src_dir_normalized = os.path.normpath(src_dir)
        dst_dir_normalized = os.path.normpath(dst_dir)
        if src_dir_normalized == dst_dir_normalized:
            e = DirectoryUtility.SourceAndDestintionSame(
                f'Source {src_dir} and destination {dst_dir} are the same.'
            )
            return [], [(src_dir, e)]
        
        # set up results
        succeeded_files, failed_files = [], []

        # go through the list of files
        for file in filelist:
            # ignore if it is an absolute path
            if os.path.isabs(file):
                e = DirectoryUtility.FileIsAbsolutePathError(
                    f'source {file} is not copied because it is an absolute path.'
                )
                failed_files.append((file, e))
                continue

            # ignore if the file is outside of the base directory (src_dir)
            # or is the base directory itself
            file_normalized_path = os.path.normpath(file)
            if file_normalized_path == '' or file_normalized_path == '.':
                # file is the base directory itself
                e = DirectoryUtility.NotInBaseDirectory(
                    f'source {file} is the base directory (at {file_normalized_path}).'
                )
                failed_files.append((file, e))
                continue
            if file_normalized_path.startswith('..'):
                # file is outside the base directory (src_dir)
                e = DirectoryUtility.NotInBaseDirectory(
                    f'source {file} is outside base directory (at {file_normalized_path}).'
                )
                failed_files.append((file, e))
                continue

            # Special case where file is 'C:ABC'
            # TODO: Let's think about how to handle this

            # get the full path of both the source and destination
            # (Should file_normalized_path be used instead of file?)
            src_path = os.path.join(src_dir, file)
            dst_path = os.path.join(dst_dir, file)

            # create the destination directory, if not already exists
            dst_dirname = os.path.dirname(dst_path)
            try:
                DirectoryUtility.create_directory(dst_dirname)
                #if verbose:
                #    print(f'created {dst_dirname}.', file=ferr)
            except NotADirectoryError as e:
                failed_files.append((file, e))
                continue

            # copy the file from source to destination
            try:
                DirectoryUtility.copy_single_file(src_path, dst_path)
            except DirectoryUtility.NotAFileError as e:
                failed_files.append((file, e))
                continue
            except FileNotFoundError as e:
                failed_files.append((file, e))
                continue
            except shutil.SameFileError as e:
                failed_files.append((file, e))
                continue

            # successful copy
            succeeded_files.append((file, file_normalized_path))
            if verbose:
                print(f'copied {src_path} to {dst_path}.', file=ferr)

        return succeeded_files, failed_files
    
    @staticmethod
    def pretty_print_copy_files_result(succeeded_files, failed_files, fout=sys.stdout):
        '''
        Print the result of copy_files() function in a pretty format

        :param succeeded_file: the first list returned by copy_files() function
        :param failed_files: the second list returned by copy_files() function
        :type succeeded_file: list of tuple
        :type failed_files: list of tuple

        :param fout: the file id to print the output to
        :type fout: file id, optional

        :return: nothing is returned by this function
        '''
        if len(succeeded_files) > 0:
            for (file, normalized_path) in succeeded_files:
                print(f'{file} -> {normalized_path}', file=fout)
        else:
            print(f'no file copied', file=fout)
        print()
        if len(failed_files) > 0:
            for (file, error) in failed_files:
                print(f'{file}: {error}', file=fout)
        else:
            print(f'no error while copying', file=fout)
        return
    
    # --- Supporting Functions Group 1
    #     - output info/error messages to stderr
    
    @staticmethod
    def get_relative_path_list(path_list: str, dirname: str,
                               verbose=False, ferr=sys.stderr):
        path_list = [os.path.relpath(path, dirname) for path in path_list]
        return path_list
    
    @staticmethod
    def normalized_path(path: str):
        return os.path.normpath(path)
    
    # --- Supporting Functions Group 2
    #     - raise Exception to indicate error
    #     - called by main API using try-except
    
    @staticmethod
    def copy_single_file(src_path: str, dst_path: str):
        # error if source does not exist
        if not os.path.exists(src_path):
            raise FileNotFoundError(
                f'source {src_path} does not exists.'
            )
        # error if source is not a file
        if not os.path.isfile(src_path):
            raise DirectoryUtility.NotAFileError(
                f'source {src_path} exists but is not a file.'
            )
        # error if destination exists and is not a file
        if os.path.exists(dst_path):
            if not os.path.isfile(dst_path):
                raise DirectoryUtility.NotAFileError(
                    f'destination {dst_path} exists and is not a file.'
                )
        # do the copy
        shutil.copyfile(src_path, dst_path)
        return
    
    @staticmethod
    def create_directory(dir_path: str):
        # error if dir_path exists and is not a directory
        if os.path.exists(dir_path):
            if not os.path.isdir(dir_path):
                raise NotADirectoryError(
                    f'{dir_path} exists and is not a directory.'
                )
        else:
            os.makedirs(dir_path, exist_ok=True)
        return
    
    ## --- Support for glob in older version of Python
    @staticmethod
    def get_glob_kwargs(include_hidden=False):
        result = {}
        if DirectoryUtilityConfig.config['hidden'] == True:
            result['include_hidden'] = include_hidden
        return result
    
class DirectoryUtilityConfig:
    '''
    Store the current configuration of the system and to provide some
    backward compatibility for the directory utilities.
    '''

    config = {
        'hidden': False
    }
    '''
    (Internal) A singleton that stores the currect configuration of the
    system and is used by the DirectoryUtility class.

    :meta private:
    '''

    @staticmethod
    def configure():
        '''
        Check and set the configuration

        :return: nothing is returned by this function
        '''
        DirectoryUtilityConfig.config['hidden'] = DirectoryUtilityConfig.check_glob_include_hidden()
        if DirectoryUtilityConfig.config['hidden'] != True:
            print(
                f'Warning: Hidden file/directory option not supported in glob in this version of python.',
                file=sys.stderr
            )
        return

    @staticmethod
    def check_glob_include_hidden():
        '''
        (Internal) Check whether the hidden file option is supported in this version of
        Python.

        Hidden file option is supported by Python 3.11 and later.

        :meta private:
        :return: True if hidden file is supported, False otherwise
        :rtype: bool
        '''
        supported_major = 3
        supported_minor = 11
        supported = False
        python_version = sys.version_info
        if python_version.major == supported_major and python_version.minor >= supported_minor:
            supported = True
        elif python_version.major > supported_major:
            supported = True
        return supported

DirectoryUtilityConfig.configure()

# --- end of file --- #
