# Usage:
# Have `get_sqls()' function in the top of this module.
# The format should be like this:
#
# sqls = [
#     "SELECT COUNT (*) FROM \"T0\" WHERE junk = 1;",  # No format characters
#     ...
# ]
#
# Note:
# Have a good use of Util.get_str_allpairs()

import Config
import Util


def get_sqls():
    sqls = []
    # Example:
    # sqls += get_str_allpairs(
    #     "SELECT * FROM \"%s\" WHERE col1 = %d;",
    #     [["T0", "T1"], [0, 1]],
    # )[:]  # Add to sqls in flat manner
    return sqls
