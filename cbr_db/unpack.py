import os
from zipfile import ZipFile

from .conf import settings
from .filesystem import get_public_data_folder
from .make_url import get_ziprar_filename
import subprocess


def get_local_ziprar_filepath(isodate, form):
    dir_ = get_public_data_folder(form, 'rar')
    filename = get_ziprar_filename(isodate=isodate, form=form)
    print("File:", filename)
    return os.path.join(dir_, filename)


def unpack(isodate, form):
    # not todo - may omit 'destination_directory' form here
    filepath = get_local_ziprar_filepath(isodate, form)
    unpack_path(filepath, form)


def unpack_path(filepath, form):
    destination_directory = get_public_data_folder(form, 'dbf')
    ext = os.path.splitext(filepath)[1].lstrip('.').lower()
    # Make sure target directory exists.
    # NOTE: `unrar e` may do nothing if target directory does not exist.
    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)
    if not os.path.isfile(filepath):
        print("File not found: {}".format(filepath))
        return
    if ext == 'rar':
        _unpack_rar(filepath, destination_directory)
    elif ext == 'zip':
        _unpack_zip(filepath, destination_directory)
    else:
        raise Exception('Unsupported archive type: {}'.format(filepath))


def _unpack_rar(filepath, destination_dir):
    subprocess.check_call([
        settings.UNPACK_RAR_EXE,
        'e', filepath,
        destination_dir,
        '-y'
    ])


def _unpack_zip(filepath, destination_dir):
    with ZipFile(filepath, 'r') as file:
        file.extractall(destination_dir)


def in_quotes(str):
    return '"' + str + '"'
