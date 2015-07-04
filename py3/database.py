# 2015-05-29 02:39 PM
# mysql, mysqlimport, mysqldump wrappers to execute *.sql files,
# mysql* must have valid ini or cfg file with credentials
#

from terminal import terminal
from conn import execute_sql, get_mysql_connection
from global_ini import DB_NAMES, DIRLIST, ACCOUNT_NAMES_DBF, BANK_NAMES_DBF
from global_ini import get_bank_name_parameters, get_account_name_parameters
from make_csv import list_csv_filepaths_by_date, get_records
from cli_dates import get_date
import os
import re

################################################################
#             0. Generic functions used in other calls         #
################################################################


###############################################################################
# mysql.exe wrapppers
###############################################################################

def run_sql_string(string, database=None, verbose=False):
    """
    Runs <string> as command for mysql.exe
    Notes:
       Requires mysql to be in PATH - see ini.bat/ini.py. Also requires host/port/user/password credentials MySQL configureation files.
       Allows running non-SQL commands in mysql.exe (e.g. source)
       For SQL commands may also use conn.execute_sql()
    """
    if database is None:
        call_string = "mysql -e \"{0}\"".format(string)
    else:
        call_string = "mysql --database {0} --execute \"{1}\"".format(
            database, string)

    # todo: -v not showing to screen, check if it so, change
    if verbose:
        call_string = call_string + " -v"

    terminal(call_string)

def get_forward_slashed_path(path):
    new_path = path.replace('\\', '/')
    return new_path

def source_sql_file(sql_filename, db_name):
    path = get_forward_slashed_path(sql_filename)
    command = r"source {0}".format(path)
    run_sql_string(command, database=db_name)

###############################################################################
# mysqlimport wrapppers
###############################################################################

def import_generic(database, path):
    if os.path.isfile(path):
        call_string = "mysqlimport {0} {1} --delete".format(database, path)
        terminal(call_string)
    else:
        print("File not found:",  path)

def mysqlimport(db_name, csv_path, ignore_lines = 1, add_mode = "ignore"):
    command_line = r'mysqlimport --ignore_lines={0} --{1} {2} "{3}" --lines-terminated-by="\r\n"'.format(
                    ignore_lines, add_mode, db_name, csv_path)
    run_mysqlimport_command_line(csv_path, command_line)

def run_mysqlimport_command_line(csv_path, command_line):
    if os.path.isfile(csv_path):
        terminal(command_line)
    else:
        print("File not found:",  csv_path)

###############################################################################
# mysqldump wrapppers
###############################################################################

def dump_table_csv(db, table, directory):
    """
    Saves database table in specified directory as csv file.
    """
    call_string = r'mysqldump --fields-terminated-by="\t" --lines-terminated-by="\r\n" --tab="{0}" {1} {2}'.format(
        directory, db, table)
    terminal(call_string)
    # Note: below is a fix to kill unnecessary slashes in txt file.
    replace_in_file(os.path.join(directory, table + ".txt"), "\\", "")
    # more cleanup, delete extra sql files:
    extra_sql = os.path.join(directory, table + ".sql")
    os.remove(extra_sql)

def dump_table_sql(db, table, path):
    """
    Dumps table from database to local directory as a SQL file.
    """
    string = r'mysqldump {0} {1} --add-drop-table=FALSE --no-create-info --insert-ignore > "{2}"'.format(
        db, table, path)
    terminal(string)


def replace_in_file(filepath, replace_what, replace_with):
    """
    Replaces 'replace_what' string with 'replace_with' string in filepath.
    Auxillary procedure used to clean up myslqdump csv output.
    """
    with open(filepath) as f:
        lines = f.read().replace(replace_what, replace_with)

    with open(filepath, 'w') as f1:
        f1.write(lines)


def read_values_from_file(regn_file, sep=","):
    """
    Reads the values contained in <regn_file>, returning a list where each
    element is a list corresponding to one line of <regn_file> that was
    split using <sep>.
    """
    with open(regn_file) as f:
        data = []

        for line in f:
            data.append(line.split(sep))

        return data

################################################################
#            1. General database operations                    #
################################################################


def delete_and_create_db(db_name):
    """
    Deletes an existing database and recreates it (empty).
    """
    print("Database:", db_name)
    command = "DROP DATABASE IF EXISTS {0}; CREATE DATABASE  {0};".format(
        db_name)
    # sql-only, using pymysql connection for this
    execute_sql(command)
    print(
        "Deleted existing database and created empty database under same name.")


def get_db_dumpfile_path(db_name):
    """
    Returns the path to sql dump files, configured in DIRLIST in the
    global initialization module.
    """
    directory = DIRLIST['global']['database']
    sql_filename = db_name + ".sql"
    path = os.path.join(directory, sql_filename).replace("\\","/")
    # path.replace(\\", '/')
    return path


def load_db_from_dump(db_name):
    """
    Loads a database structure from a dump file.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    """
    print("Database:", db_name)
    path = get_db_dumpfile_path(db_name)
    source_sql_file(path, db_name)
    print("Loaded database structure from file <{0}.sql>. No data was imported.".format(
        db_name))


def save_db_to_dump(db_name):
    """
    Saves the structure of a database to a sql dump file in the standard location.
    Standard location defined by get_db_dumpfile_path()
    # todo: change to new directory structure
    # Other variety: http://code.activestate.com/recipes/286223-ohmysqldump/
    """
    print("Database:", db_name)
    # uses mysqldump and terminal()
    path = get_db_dumpfile_path(db_name)
    #               mysqldump %1  --no-data --routines > %1.sql
    line_command = "mysqldump {0} --no-data --routines > {1}".format(db_name, path)
    terminal(line_command)
    print("Dumped database structure to file <{0}.sql>. No data saved to this file.".format(
        db_name))

def clear_table(db, table):
    """
    Removes all entries from <table> at <db>.
    """
    conn = get_mysql_connection(database=db)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM `{}`".format(table))
        conn.commit()
        cur.close()
    finally:
        conn.close()

def make_insert_statement(table, fields, ignore=False):
    """
    Creates an insert SQL statement that insert a row into <table> using
    columns <fields>. The statement is built using placeholders (%s) to use
    to ensure proper value quoting.
    If <ignore> is True, then rows with repeated primary keys will be
    ignored.
    """
    mode = "IGNORE" if ignore else ""

    insert_sql = "INSERT {} INTO {} ({}) VALUES ({})".format(
        mode,
        table,
        ",".join(fields),
        ",".join(["%s"]*len(fields))
    )

    return insert_sql

def insert_rows_into_table(db, table, fields, values, ignore=False):
    """
    Inserts <values> into <db> <table> <fields>. Should only be used when
    <values> are  small enought for all values to fit in memory. If ignore is
    True, duplicates will be ignored.
    """
    sql = make_insert_statement(table, fields, ignore)
    conn = get_mysql_connection(database=db)

    try:
        cur = conn.cursor()

        for row in values:
            cur.execute(sql, row)

        conn.commit()
    finally:
        cur.close()
        conn.close()

################################################################
#                  2. DBF and TXT file import                  #
################################################################

def import_csv(isodate, form):
    db_name = DB_NAMES['raw']
    for csv_path in list_csv_filepaths_by_date(isodate, form):
        mysqlimport(db_name, csv_path, ignore_lines=1)

    print("\nFinished importing CSV files into raw data database.")
    print("Form:", form, "Date:", isodate)

from global_ini import get_private_data_folder

def import_csv_derived_from_text_files(form):
    db_name = DB_NAMES['raw']

    directory = get_private_data_folder(form, 'csv')

    for filename in os.listdir(directory):
        csv_path = os.path.join(directory, filename)
        mysqlimport(db_name, csv_path, ignore_lines=0)

    print("\nFinished importing CSV files into raw data database.")
    print("Directory:", directory)


################################################################
#              3. Dataset manipulation                         #
################################################################

def read_table_sql(db, form, file):
    """
    Support function, it is not called directly from the interface.
    todo: refactor?
    """
    path = os.path.join(DIRLIST[form]['output'], file)
    source_sql_file(path, db)


def get_sqldump_table_and_filename(form):
    """
    Returns (f101, f101.sql) for form 101, and similar output for other forms.
    Support function, it is not called directly from the interface.
    """
    table = 'f' + form
    file = table + ".sql"
    return table, file


def save_dataset_as_sql(form):
    """
    Saves the dataset corresponding to *form* to the default sql dump file.
    """
    database = DB_NAMES['raw']
    table, file = get_sqldump_table_and_filename(form)
    path = os.path.join(DIRLIST[form]['output'], file)
    dump_table_sql(database, table, path)


def import_dataset_from_sql(form):
    """
    Imports a dataset from the default sql dump file.
    """
    database = DB_NAMES['final']
    _, file = get_sqldump_table_and_filename(form)
    read_table_sql(database, form, file)


def create_final_dataset_in_raw_database(form, timestamp1, timestamp2=None,
                                         regn_list=None, regn_file=None,
                                         regn_all=True):
    """
    Processes the data from the raw database, creating the final dataset for
    <form>.
    <timestamp1> and <timestamp2> can be set to limit the dates that goes
    to the final dataset.

    <regn_list> can be set to a string containing the registration numbers,
    separated by comma, that will be selected to the final database.

    <regn_file> (optional) can be the path to a file containing the registration
    numbers, one in each line of the file.

    If <regn_all> is True, all possible registration numbers can be selected to
    go to the final database.

    Only one regn selection mechanism should be set at the same time. Priority is
    given in this order: <regn_list>, <regn_file>, and <regn_all>. If no regn
    mechanism was selected, <regn_all> is used.
    """
    db = DB_NAMES["raw"]

    # date handling
    clear_table(db, "cfg_date_limit")

    def to_date(x):
        try:
            return get_date(x)[0]
        except:
            return None

    insert_rows_into_table(
        db=db,
        table="cfg_date_limit",
        fields=('dt_start', 'dt_end'),
        values=[(to_date(timestamp1), to_date(timestamp2))]
    )

    run_sql_string("call cfg_init_populate_dates();", db)

    # regn handling
    clear_table(db, "cfg_regn_in_focus")
    
    if not regn_list and not regn_file:
        regn_all = True

    if not regn_all:
        # get regn list and insert it to the database
        if regn_list:
            regn = regn_list.split(',')
        elif regn_file:
            try:
                # try reading from the current work directory
                regn = read_values_from_file(regn_file)
            except FileNotFoundError:
                try:
                    # try in the global tables dir
                    dir_ = DIRLIST['global']['tables']
                    path = os.path.join(dir_, regn_file)
                    print('-> {} was not found in the work dir. Trying in {}'.format(
                        regn_file, path))

                    regn = read_values_from_file(path)
                except FileNotFoundError:
                    print("-> {} not found, aborting".format(regn_file))
                    return

        insert_rows_into_table(
            db=db,
            table="cfg_regn_in_focus",
            fields=('regn', ),
            values=regn
        )
    else:
        # populate all regn from a stored procedure
        run_sql_string("call cfg_init_regn_fullset();", db)

    # make the final dataset in the raw database
    run_sql_string("call f{}_make_dataset();".format(form), db)

################################################################
#             4. Working with the final dataset               #
################################################################

def import_dbf_generic(dbf_path, db, table, fields, dbf_fields=None):
    """
    Imports a dbf file to a database directly, without using temporary files.
    The dbf file is located at <dbf_path>, and the data is imported to
    <db>.<table>, using fields <fields>. Repeated rows (same primary key) are
    ignored by default.
    """
    fields = list(fields)  # to accept generators

    # table fields can be different from the dbf fields
    if dbf_fields is None:
        dbf_fields = fields

    insert_sql = make_insert_statement(table, fields, ignore=True)

    # with autocommit turned off, the insertions should be fast
    conn = get_mysql_connection(database=db, autocommit=False)

    try:
        cur = conn.cursor()

        for record in get_records(dbf_path, dbf_fields):
            ordered_values = [record[key] for key in dbf_fields]
            cur.execute(insert_sql, ordered_values)

        conn.commit()
        cur.close()
    finally:
        conn.close()

def get_import_dbf_path(target, form):
    """
    Returns the path to the dbf file that contains the bank or account names
    for <form> to be imported to the final database. <target> can be "bank"
    (for dbf with bank names) or "plan" (for dbf with account names).
    
    When <target> is "plan", a single string is returned. When <target> is "bank",
    a list with two strings is returned, pointing to two distinct dbf files.
    """
    name = None

    if target == "plan":
        name = ACCOUNT_NAMES_DBF[form]
    elif target == "bank":
        if form in ('101', '102'):
            tops = [] # two different patterns        
            
            for pattern in BANK_NAMES_DBF:
                expr = re.compile(pattern)
                dir_ = DIRLIST['101']['dbf']
                cand = []            
                
                for file in os.listdir(dir_):
                    r = expr.search(file)
                    if r:
                        cand.append(r.string)
                
                cand.sort(key=lambda x: (x[2:6], x[0:2]), reverse=True)
                tops.append(os.path.join(dir_, cand[0]))
                
            return tops
        else:
            raise ValueError("Invalid form / form not implemented yet")
    else:
        raise ValueError("Invalid target")

    return os.path.join(DIRLIST[form]['dbf'], name)

def import_plan(form):
    """
    Imports account names of <form> into the final database, removing all
    previous entries.
    """
    db = DB_NAMES['final']
    dbf = get_import_dbf_path('plan', form)
    table, fields, dbf_fields = get_account_name_parameters(form)
    
    print("Importing account names from {}...".format(dbf))    
    
    clear_table(db, table)
    import_dbf_generic(dbf, db, table, fields, dbf_fields)
    
    print("-> Done.")
    
def import_bank():
    """
    Imports bank names into the final database, removing all
    previous entries.
    """
    form = '101'
    db = DB_NAMES['final']
    dbf_names = get_import_dbf_path('bank', form)
    table, fields_list, dbf_fields_list = get_bank_name_parameters()

    clear_table(db, table)
    
    for dbf_name, fields, dbf_fields in zip(dbf_names, fields_list, dbf_fields_list):
        print("Importing bank names from {}".format(dbf_name))
        import_dbf_generic(dbf_name, db, table, fields, dbf_fields)
        print("-> Done")

def import_alloc(filename='alloc_raw.txt'):
    """
    TODO: describe what this function does
    """
    database = DB_NAMES['final']
    path = os.path.join(DIRLIST['global']['alloc'], filename)
    import_generic(database, path)


def import_tables():
    """
    TODO: describe what this function does
    """
    database = DB_NAMES['final']
    directory = os.path.join(DIRLIST['global']['tables'])

    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if file.endswith(".txt"):
            import_generic(database, path)
        if file.endswith(".sql"):
            source_sql_file(path, database)
            # Risk: import_generic and source_sql_file - similar functions
            # different arg order

def make_balance():
    """
    TODO: describe what this function does
    """
    db_name = DB_NAMES['final']
    execute_sql("call alloc_make", db_name)
    execute_sql("delete from balance", db_name)
    execute_sql("call balance_make", db_name)
    # use cbr_db2;
    # call alloc_make;
    # delete from balance;
    # call balance_make;

def test_balance():
    """
    TODO: describe what this function does
    """
    def do_output(sql):
        print('-> ' + sql)
        out = execute_sql(sql, DB_NAMES['final'], verbose=False)
        # Risk: I see no valuable info with verbose=True, as I'm printing the results here
        if out:
            for row, val in enumerate(out, 1):
                print("row {0}: {1}".format(row, val))
        else:
            print('No output')

        print()

    do_output('select "Test: balance residuals" as Test')
    do_output('select * from test_balance_residual')
    do_output('select "Test: ref items" as Test')
    do_output('select * from test_ref_items')
    do_output('select "Test: net assets not zero" as Test')
    do_output(
        'select dt, regn, itogo from balance where line = 500 and itogo != 0 order by dt')

from make_xlsx import make_xlsx

def report_balance_tables_xls():
    """
    TODO: describe what this function does
    """
    report_balance_tables_csv()
    directory = DIRLIST['101']['output']
    make_xlsx(directory)

def report_balance_tables_csv():
    """
    TODO: describe what this function does and change wording
    """
    # prepare TABLES in database
    db_name = DB_NAMES['final']
    execute_sql("call balance_report_line_dt_3tables", db_name)

    # dump TABLES to CSV
    directory = DIRLIST['101']['output']
    TABLES = ("tmp_output_itogo", "tmp_output_ir", "tmp_output_iv")
    for table in TABLES:
        dump_table_csv(db_name, table, directory)
