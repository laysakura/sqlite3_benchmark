# Some of these parameters are overwritten by command line options

import os
basedir = os.path.dirname(os.path.abspath(__file__)) + "/.."

## Benchmark targets
# sqlite3Path = "/path/to/sqlite3"
# sqlite3DbPath = "%s/inputDb/foo.sqlite" % (basedir)

## Results holder
resultsDbPath = "%s/resultsDb/results.sqlite" % (basedir)
resultsDbTable = "results"

## Benchmark timer
timeOutputPath = "/tmp/sqlite_benchmark.txt"
timeCmd = "/usr/bin/time -p --output=%s" % (
    timeOutputPath)

## SQLite settings
sqlite3Encoding = 'utf-8'

## Page cache management
dropPageCache = False
dropPageCacheCmd = "/path/to/dropPageCache_script"
sleepAfterDropPageCache = 0.5  # exec time varies without sleep?

## Whether to show the output.
## Note that showing output can slow performance down.
showStdout = False
showStderr = True

## Graph settings
graphXlabel = "SQL"
graphYlabel = "Time [sec]"
graphTerminal = "postscript eps enhanced color \"GothicBBB-Medium-UniJIS-UTF8-H\""

## App specifics.
## Write some setting parameters used by SQL.py
