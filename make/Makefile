include _para_sweep_rules.mk  # You can hit `make' command only in this directory.


### Parameter definitions ###
parameters:=dbPath dropPageCache trial

dbPath:=../inputDb/foo.sqlite ../inputDb/bar.db
dropPageCache:=0 1
trial:=$(shell seq 2)


### Check if finished ###
output=done/dbPath_$(shell perl -MDigest::MD5 -le "print Digest::MD5::md5_hex(\"$(dbPath)\")")--dropPageCache_$(dropPageCache)--trial_$(trial)


### Run Command ###
cmd=\
  ../python/sqlite-benchmark.py --dbPath=$(dbPath) --dropPageCache=$(dropPageCache) && \
  touch $(output)

$(define_rules)


clean:
	$(RM) done/*
	$(RM) -i ../resultsDb/results.sqlite
