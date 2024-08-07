# file: dir_util.py

import os
import sys
import shutil
from glob import glob

class DirectoryUtility:

    # --- Exceptions defined in this module

    class SourceAndDestintionSame(Exception):
        pass

    class NotAFileError(Exception):
        pass

    class FileIsAbsolutePathError(Exception):
        pass

    class NotInBaseDirectory(Exception):
        pass

    # --- Main API for this modules

    @staticmethod
    def list_files(dirname: str, filename_pattern: str,
                   recursive=False, include_hidden=False, get_relative_path=False,
                   verbose=False, ferr=sys.stderr):
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

    config = {
        'hidden': False
    }

    @staticmethod
    def configure():
        DirectoryUtilityConfig.config['hidden'] = DirectoryUtilityConfig.check_glob_include_hidden()
        if DirectoryUtilityConfig.config['hidden'] != True:
            print(
                f'Warning: Hidden file/directory option not supported in glob in this version of python.',
                file=sys.stderr
            )
        return

    @staticmethod
    def check_glob_include_hidden():
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
