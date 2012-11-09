# Some of these parameters are overwritten by command line options

import os
basedir = os.path.dirname(os.path.abspath(__file__)) + "/.."

## Benchmark targets
# sqlite3Path = "/path/to/sqlite3"
# sqlite3DbPath = "/home/nakatani/git/evolution_benchmark/folders.db"

## Results holder
resultsDbName = "results.sqlite"
resultsDbPath = "%s/resultsDb/%s" % (basedir, resultsDbName)
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

## App specifics.
## Write some setting parameters used by SQL.py
