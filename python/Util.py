import sys
from subprocess import Popen, PIPE


def _wait_with_check(process):
    check_prefix = "[wait_with_check] "
    process.wait()
    retcode = process.returncode
    if retcode < 0:
        sys.stderr.write(
            "------\n%sProcess %s was stopped by signal#%d\n%s\n------" %
            (check_prefix,
             process,
             -retcode,
             process.stderr.read()))
        exit(1)
    elif retcode > 0:
        sys.stderr.write(
            "------\n%sProcess %s returned exit code #%d\n%s\n------" %
            (check_prefix,
             process,
             retcode,
             process.stderr.read()))
        exit(1)


def sh_cmd_sync(cmd):
    """
    @example
    (stdout_str, stderr_str) = sh_cmd_sync("ls")
    """
    p = Popen(
        cmd,
        shell=True,
        stdout=PIPE,
        stderr=PIPE)
    _wait_with_check(p)
    stdout_str = p.stdout.read()
    stderr_str = p.stderr.read()
    return (stdout_str, stderr_str)


def _allpairs(h, t, result_list):
    _h = h[:]
    _t = t[:]
    if len(_t) == 0:
        result_list.append(_h)
        return
    headPair = _t[0]
    _h.append(None)
    for headPairElem in headPair:
        _h[len(_h) - 1] = headPairElem
        _allpairs(_h, _t[1:], result_list)


def get_allpairs(l):
    """
    @note
    It is recommended to use itertools.product().

    >>> get_allpairs([[1, 2, 3], [4, 5]])
    [[1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]]
    """
    result_list = []
    _allpairs([], l, result_list)
    return result_list


def get_str_allpairs(fmt_str, fmt_list):
    """
    >>> get_str_allpairs('A%d B%s', [[1, 2, 3], ['4', '5']])
    ['A1 B4', 'A1 B5', 'A2 B4', 'A2 B5', 'A3 B4', 'A3 B5']
    """
    str_allpairs = []
    fmt_list_allpairs = get_allpairs(fmt_list)
    for l in fmt_list_allpairs:
        str_allpairs.append(fmt_str % tuple(l))
    return str_allpairs


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
