"""
This module contains interface functions to mysql processes,
such as mysqldump, mysqlimport, etc.
"""

import os
import re
import subprocess
import tempfile
import time

from cbr_db.conf import settings
from cbr_db.database.connection import get_credentials
from cbr_db.filesystem import get_db_dumpfile_path
from cbr_db.utils.text import replace_in_file


def mysqlimport_generic(database, path):
    credentials = get_credentials()
    run_process([
        'mysqlimport',
        '-u' + credentials['user'],
        '-p' + credentials['passwd'],
        '--delete',
        database,
        path,
    ])


def mysqlimport(db_name, csv_path, ignore_lines=1, add_mode='ignore'):
    credentials = get_credentials()
    # Trying to use mysqlimport without --lines-terminated-by="\r\n"
    # (this works on Debian linux on remote server)
    run_process([
        'mysqlimport',
        '-u' + credentials['user'],
        '-p' + credentials['passwd'],
        '--ignore_lines={}'.format(ignore_lines),
        '--{}'.format(add_mode),
        db_name,
        csv_path,
    ])


def run_sql_string(string, database, verbose=False):
    """
    Runs <string> as command for mysql.exe
    Notes:
       Requires mysql to be in PATH - see ini.bat/ini.py.
       Also requires host/port/user/password credentials MySQL configureation files.
       Allows running non-SQL commands in mysql.exe (e.g. source)
       For SQL commands may also use conn.execute_sql()
    """
    credentials = get_credentials()
    cmdline = [
        'mysql',
        '-u' + credentials['user'],
        '-p' + credentials['passwd'],
        '--database', database,
        '--execute', string,
    ]
    if verbose:
        cmdline.append('-v')
    run_process(cmdline)


def source_sql_file(sql_filename, db_name):
    path = sql_filename.replace('\\', '/')
    command = r"source {0}".format(path)
    run_sql_string(command, database=db_name)


def dump_table_csv(db, table, directory):
    """
    Saves database table in specified directory as csv file.
    """
    credentials = get_credentials()
    run_process([
        'mysqldump',
        '-u' + credentials['user'],
        '-p' + credentials['passwd'],
        '--fields-terminated-by="\\t"',
        '--lines-terminated-by="\\r\\n"',
        '--tab', directory,
        db,
        table,
    ])
    # Note: below is a fix to kill unnecessary slashes in txt file.
    replace_in_file(os.path.join(directory, table + ".txt"), "\\", "")
    # more cleanup, delete extra sql files:
    extra_sql = os.path.join(directory, table + ".sql")
    os.remove(extra_sql)


def dump_table_sql(db, table, path):
    """
    Dumps table from database to local directory as a SQL file.
    """
    credentials = get_credentials()
    with open(path, 'wb') as file:
        run_process([
            'mysqldump',
            '-u' + credentials['user'],
            '-p' + credentials['passwd'],
            '--add-drop-table=FALSE',
            '--no-create-info',
            '--insert-ignore',
            db,
            table,
        ], stdout=file)
    print('Table {!r}.{!r} saved to {}'.format(db, table, path))


def patch_sql_file(path):
    """
    Applies necessary patches to SQL file (such as username/password).
    Returns path to patched file (in a temp folder).
    """
    with open(path, encoding='utf-8') as file:
        text = file.read()
    credentials = get_credentials()
    text = re.sub(r"([`'])\w+[`']@[`']\w+[`']",
                  r"\1{}\1@\1%\1".format(credentials['user']),
                  text)
    tempdir = os.path.join(tempfile.gettempdir(), 'cbr-db')
    if not os.path.isdir(tempdir):
        os.makedirs(tempdir)
    temp_file_path = os.path.join(tempdir, os.path.split(path)[1])
    with open(temp_file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return temp_file_path


def mysqldump(db_name):
    credentials = get_credentials()
    print("Database: ", db_name)
    path = get_db_dumpfile_path(db_name)
    with open(path, 'wb') as file:
        run_process([
            'mysqldump',
            '-u' + credentials['user'],
            '-p' + credentials['passwd'],
            '--no-data',
            '--routines',
            db_name,
        ], stdout=file)
    print("Dumped DB schema {!r} to {}".format(db_name, path))


def run_process(cmdline, shell=False, stdout=None, stderr=None):
    # Workaround for MySQL under Windows
    if settings.IS_WINDOWS:
        cmdline[0] = _find_mysql_exe(cmdline[0])
    print('Calling: {!r}'.format(cmdline))
    start_time = time.monotonic()
    subprocess.check_call(cmdline, shell=shell, stdout=stdout, stderr=stderr)
    print("Elapsed time: {:.2f}".format(time.monotonic() - start_time))


def _find_mysql_exe(name):
    exe_name = name + '.exe'
    for path in settings.MYSQL_PATHS:
        exe_path = os.path.join(path, exe_name)
        if os.path.isfile(exe_path):
            return exe_path
    raise Exception('MySQL executable {!r} not found in paths: {!r}'
                    .format(exe_name, settings.MYSQL_PATHS))
