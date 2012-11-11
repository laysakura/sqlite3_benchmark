#!/usr/bin/env python

import smart_gnuplotter
g = smart_gnuplotter.smart_gnuplotter()
import Config
import Util


def get_graph_file_name(var_graph_file_params):
    ret = ""
    for key in var_graph_file_params.keys():
        ret += "%(key)s_%%(%(key)s)s--" % {"key": key}
    return ret[:len(ret) - len("--")]


def get_title_from_var_params(var_params):
    ret = ""
    for key in var_params.keys():
        ret += "%(key)s='%%(%(key)s)s' ; " % {"key": key}
    return ret[:len(ret) - len(" ; ")]


def _get_var_graph_file_param_names():
    (stdout_str, stderr_str) = Util.sh_cmd_sync(
        "(cd %s/make ; make --quiet show_var_graph_file_params)" %
        (Config.basedir))
    return stdout_str.split()


def _get_var_plot_param_names():
    (stdout_str, stderr_str) = Util.sh_cmd_sync(
        "(cd %s/make ; make --quiet show_var_plot_params)" %
        (Config.basedir))
    return stdout_str.split()


def _get_param_keyvals(param_names):
    ret = {}
    for key in param_names:
        value = g.do_sql(
            Config.resultsDbPath,
            "select distinct " + key + " from " + Config.resultsDbTable + ";",
            single_col=1)
        ret[key] = value
    return ret


def get_var_graph_file_params():
    param_names = _get_var_graph_file_param_names()
    return _get_param_keyvals(param_names)


def get_var_plot_params():
    param_names = _get_var_plot_param_names()
    return _get_param_keyvals(param_names)


def get_where_clause(var_graph_file_params, var_plot_params):
    ret = ""
    for g_param in var_graph_file_params:
        ret += "%(g_param)s='%%(%(g_param)s)s' and " % {"g_param": g_param}
    for p_param in var_plot_params:
        ret += "%(p_param)s='%%(%(p_param)s)s' and " % {"p_param": p_param}
    return ret[:len(ret) - len("and ")]


def get_temp_table_sql():
    return (
"""
-- Write `create temp table tmp_T0 ...'
"""
    )


def plot(var_graph_file_params, var_plot_params):
    ## Temp table definition
    init = get_temp_table_sql()

    w = get_where_clause(var_graph_file_params, var_plot_params)
    query = (
        "select 'SQL'||sql_no, avg(real_time), stdev(real_time)" +
        "  from " + Config.resultsDbTable +
        "  where " + w +
        "  group by sql_no;"
    )
    vars_dict = var_graph_file_params.copy()
    vars_dict.update(var_plot_params)
    g.graphs(
        (Config.resultsDbPath, query, init),
        terminal=Config.graphTerminal,
        output="%s/resultsGraph/%s" % (
            Config.basedir,
            get_graph_file_name(var_graph_file_params)),

        graph_attr="""
set style fill solid 1.00 border 0
set style histogram errorbars gap 2 lw 1
set style data histogram
set xtics rotate by -45
set grid ytics
""",
        graph_title=get_title_from_var_params(var_graph_file_params),
        plot_title=get_title_from_var_params(var_plot_params),
        using="2:3",
        yrange="[0:]",
        xlabel=Config.graphXlabel,
        ylabel=Config.graphYlabel,
        vars_dict=vars_dict,
        graph_vars=var_graph_file_params.keys(),
    )


def main():
    ## Get appropreate graph variable
    var_graph_file_params = get_var_graph_file_params()
    var_plot_params = get_var_plot_params()

    ## Elapsed time
    plot(var_graph_file_params, var_plot_params)


if __name__ == "__main__":
    main()
