include _para_sweep_rules.mk  # You can hit `make' command only in this directory.


### Parameter definitions ###
var_graph_file_params:=drop_page_cache
var_plot_params:=db
parameters=$(var_graph_file_params) $(var_graph_bar_params) trial

db:=foo.sqlite bar.sqlite  # Do not include fullpath as paramter values
drop_page_cache:=0 1
trial:=$(shell seq 2)


### Check if finished ###
output=done/db_$(db)--drop_page_cache_$(drop_page_cache)--trial_$(trial)


### Run Command ###
cmd=\
  ../python/sqlite-benchmark.py --dbPath=../inputDb/$(db) --dropPageCache=$(drop_page_cache) && \
  touch $(output)

$(define_rules)


### Other Rules ###
clean:
	$(RM) done/*
	$(RM) -i ../resultsDb/results.sqlite

show_var_graph_file_params:
	@echo $(var_graph_file_params)
show_var_plot_params:
	@echo $(var_plot_params)
