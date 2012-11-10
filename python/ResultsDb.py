import Config
from TimeOutputParser import TimeOutputParser
from datetime import datetime
import sqlite3
import os


def _get_last_time_result_dict():
    """
    @return
    None if failed to get the last result of time command.
    """
    # if os.path.exists(Config.timeOutputPath):
    #     return None
    parser = TimeOutputParser(Config.timeOutputPath)
    return parser.get_dict()


def get_row_dict(sql, sql_no):
    row_dict = {}

    row_dict["sql"] = sql
    row_dict["sql_no"] = sql_no
    row_dict["db"] = os.path.basename(Config.sqlite3DbPath)
    row_dict["drop_page_cache"] = int(Config.dropPageCache)
    row_dict["timestamp"] = datetime.now()

    time_dict = _get_last_time_result_dict()
    row_dict.update(time_dict)

    return row_dict


def pretty_print_row(stdout_str,
                     stderr_str,
                     row_dict):
    output = (
"""
==================================
[Benchmark settings]
timestamp = %(timestamp)s
dbFile = %(db)s
sql = [SQL%(sql_no)d] %(sql)s
dropPageCache = %(drop_page_cache)d

[Benchmark results]
(real, user, sys) = (%(real_time)f, %(user_time)f, %(sys_time)f)
""" % row_dict
    )

    if Config.showStdout:
        output += (
"""
[SQLite outputs]
%s
""" % stdout_str
        )

    if Config.showStderr and stderr_str != "":
        output += (
"""
[SQLite errors]
%s
""" % stderr_str
        )

    print(output)


def insert(row_dict):
    conn = sqlite3.connect(Config.resultsDbPath)
    cursor = conn.cursor()

    col_names = ""
    col_values = []
    bindings = ""
    for key, val in row_dict.iteritems():
        col_names += "%s," % (key)
        # Inserting data using sqlite3 module requires unicode object.
        if isinstance(val, str):
            val = unicode(val, Config.sqlite3Encoding)
        col_values.append(val)
        bindings += "?,"
    col_names = col_names[:len(col_names) - 1]  # omit last comma
    bindings = bindings[:len(bindings) - 1]

    sql = u"insert into %s (%s) values (%s)" % (
        Config.resultsDbTable, col_names, bindings)
    cursor.execute(sql, tuple(col_values))
    conn.commit()

    cursor.close()
    conn.close()


def create_if_not_exist():
    # TODO: how to make table schema easy to reconfigure?
    schema_ddl = (
"""
create table if not exists %s (
    timestamp DATETIME NOT NULL,
    db TEXT NOT NULL,
    sql TEXT NOT NULL,
    sql_no INT NOT NULL,
    drop_page_cache INT NOT NULL,
    real_time REAL NOT NULL,
    user_time REAL NOT NULL,
    sys_time REAL NOT NULL
);
""" % (Config.resultsDbTable)
    )
    conn = sqlite3.connect(Config.resultsDbPath)
    cursor = conn.cursor()

    cursor.execute(schema_ddl)

    cursor.close()
    conn.close()
