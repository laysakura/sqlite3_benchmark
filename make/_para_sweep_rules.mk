#
# usage:
# (1) write a Makefile that looks like 
#
# include ps.mk
# parameters:=x y z
# 
# output=result_$(x)_$(y)_$(z)
# cmd=foo $(x) $(y) $(z) > $(output)
#
# x:=1 2 3
# y:=a b
# z:=p q
# $(define_rules)
#
# (2) then run make:
#   make (or make -j xxx for parallel run)
# it will run all the combinations 3x2x2=12 commands
#
# foo 1 a p > result_1_a_p
# foo 1 a q > result_1_a_q
# foo 1 b p > result_1_b_p
# foo 1 b q > result_1_b_q
# foo 2 a p > result_2_a_p
# foo 2 a q > result_2_a_q
# foo 2 b p > result_2_b_p
# foo 2 b q > result_2_b_q
# foo 3 a p > result_3_a_p
# foo 3 a q > result_3_a_q
# foo 3 b p > result_3_b_p
# foo 3 b q > result_3_b_q

#
#
# 
# [1] define rule templates
# 

#
# $(call expand_parameters,a b c)
#  ==> .$(a).$(b).$(c)
#

define expand_parameters
$(if $(1),.$$($(firstword $(1)))$(call expand_parameters,$(wordlist 2,$(words $(1)),$(1))))
endef

define make_rule_single
$(target) : $(output)
$(output) : $(input)
	$(cmd)
endef

# a:=1 2
# b:=3 4 
# $(call make_rule_recursive,a b)
#  ==> $(foreach a,1 2,$(call make_rule_recursive,b))
#   ==> $(foreach a,1 2,$(foreach b,3 4,$(call make_rule_recursive)))
#    ==> $(foreach a,1 2,$(foreach b,3 4,$(eval $(call make_rule_single))))
#  
define make_rule_recursive
$(if $(1),\
  $(foreach $(firstword $(1)),\
            $($(firstword $(1))),\
     $(call make_rule_recursive,$(wordlist 2,$(words $(1)),$(1)))),\
  $(eval $(call make_rule_single)))
endef

# 
# [2] set default parameters
# 

target:=$(or $(target),gxp_pp_default_target)

$(target) : 

#
# [3] really define rules
#

define define_rules_fun
$(if $(and $(parameters),$(cmd),$(output)),\
  $(eval $(call make_rule_recursive,$(parameters))),\
  $(warning "specify at least parameters:=..., cmd=..., and output=..."))
endef

define_rules=$(call define_rules_fun)

$(and $(parameters),$(cmd),$(output),$(define_rules))

