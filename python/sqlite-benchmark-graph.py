#!/usr/bin/env python

import smart_gnuplotter
g = smart_gnuplotter.smart_gnuplotter()
import sys
import os
import Config


def parse_args():
#     if len(sys.argv) != 2:
#         print("""
# ARGS:  TABLE_NAME

# Here are the candidate tables:
# """)
#         os.system("sqlite3 %s '.schema'" % (db_path))
#         exit(1)
    return sys.argv[1]


def get_temp_table_sql():
    return (
"""
-- Write `create temp table tmp_T0 ...'
"""
    )


def main():
    # table_name = parse_args()

    ## Temp table definition
    init = get_temp_table_sql()

    ## Get appropreate graph variable
    dbPath_list = g.do_sql(
        Config.resultsDbPath,
"""
select distinct dbPath from %(resultsDbTable)s;
""" % {
    "resultsDbTable": Config.resultsDbTable,
},
        single_col=1)
    # n_lines_list = g.do_sql(db_path, "select distinct n_lines from " + table_name, single_col=1)
    # block_factor_list = g.do_sql(db_path, "select distinct block_factor from " + table_name, single_col=1)

    ## Elapsed time
    query = (
"""
select sql, avg(real_time) from %(resultsDbTable)s
group by sql;
""" % {
    "resultsDbTable": Config.resultsDbTable,
}
    )
    g.graphs(
        (Config.resultsDbPath, query, init),
        # output="graphs/serial_%(M)s",
        # graph_title="$M=%(M)s$",
        # graph_title="graph_title",
        # plot_title="%(typ)s",
        plot_title="%(dbPath)s",
        plot_with="histogram fs solid 0.9",
        using="2",
        yrange="[0:]",
        xlabel="Program",
        ylabel="Performance (GFLOPS)",

        dbPath=dbPath_list,
        #graph_vars=[ "M"]
        )


    # g.graphs((Config.resultsDbPath, query, init),
    #          # plot_title="n_lines=%(n_lines)s block_factor=%(block_factor)s",
    #          plot_with="lp",
    #          xlabel="# Nodes",
    #          ylabel="Elapsed Time [sec]",
    #          yrange="[0:]",
    #          # n_lines=n_lines_list,
    #          # block_factor=block_factor_list
    #          )



    ## Speedup
#     query = '''
# select n_clients, avg(serial_udx_time / udx_time)
# from ''' + table_name + '''_for_scalability
# where
#   n_lines = %(n_lines)s
# group by
#   n_clients
# '''
#     g.graphs((db_path, query, init),
#              plot_title="n_lines=%(n_lines)s",
#              plot_with="lp",
#              xlabel="# Nodes",
#              ylabel="Scalability",
#              overlays=[("x", { "plot_title" : "ideal" })],
#              n_lines=n_lines_list)


if __name__ == "__main__":
    main()
