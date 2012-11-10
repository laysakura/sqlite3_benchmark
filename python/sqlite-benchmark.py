#!/usr/bin/env python

import time
import Config
import Util
import SQL
import ResultsDb


def parse_args():
    import argparse

    # create the parser
    parser = argparse.ArgumentParser(description="SQLite3 benchmark tool")

    parser.add_argument(
        "--dbPath",
        default=None,
        help="SQLite3 DB path")
    parser.add_argument(
        "--dropPageCache",
        type=int,
        default=0,
        metavar="0/1",
        help="Whether to drop page cache before executing each SQL")

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    overwrite_config(args)


def overwrite_config(args):
    if args.dbPath is not None:
        Config.sqlite3DbPath = args.dbPath
    Config.dropPageCache = bool(args.dropPageCache)


def load_db_on_page_cache(db_path):
    Util.sh_cmd_sync("cat %s > /dev/null" % (db_path))


def drop_page_cache_if_necessary():
    if Config.dropPageCache:
        Util.sh_cmd_sync(Config.dropPageCacheCmd)
        time.sleep(Config.sleepAfterDropPageCache)


def get_sql_cmdline(sql):
    cmd = "%s %s %s '%s'" % (
        Config.timeCmd,
        Config.sqlite3Path,
        Config.sqlite3DbPath,
        sql
    )
    if not Config.showStdout:
        cmd += " > /dev/null"
    if not Config.showStderr:
        cmd += " 2> /dev/null"
    return cmd


def issue_sqls():
    sqls = SQL.get_sqls()
    for sql in sqls:
        drop_page_cache_if_necessary()

        cmd = get_sql_cmdline(sql)
        (stdout_str, stderr_str) = Util.sh_cmd_sync(cmd)

        row_dict = ResultsDb.get_row_dict(sql)
        ResultsDb.pretty_print_row(stdout_str, stderr_str, row_dict)
        ResultsDb.insert(row_dict)


def pre_benchmark():
    parse_args()

    ResultsDb.create_if_not_exist()

    if not Config.dropPageCache:
        load_db_on_page_cache(Config.sqlite3DbPath)


def benchmark():
    issue_sqls()


def post_benchmark():
    pass


def main():
    pre_benchmark()
    benchmark()
    post_benchmark()


if __name__ == '__main__':
    main()
