###############################################################################
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# Copyright (c) 2016 Jarrett Rainier
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Potential Ventures Ltd,
#       SolarFlare Communications Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

# The most powerful language in the world is VHDL - Because it's what I know
TOPLEVEL_LANG ?= vhdl

SIM ?= ghdl

WPWD=$(shell sh -c 'pwd -W')
PWD=$(shell pwd)
COCOTB=$(PWD)/../../tools/cocotb
GPROF2DOT=$(PWD)/../../tools/gprof2dot
WWW=$(PWD)/../../tools/www

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
PYTHONPATH := $(PWD)/../cosim;$(PYTHONPATH)
else
WPWD=$(shell pwd)
PYTHONPATH := $(PWD)/../cosim:$(PYTHONPATH)
endif

ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(WPWD)/../hdl/sha1_pkg.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/sha1_load.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/sha1_process_input.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/sha1_process_buffer.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/sha1_scheduler.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/hmac_cache.vhd
    #VHDL_SOURCES += $(WPWD)/../hdl/hmac_main.vhd
    #VHDL_SOURCES += $(WPWD)/../hdl/hmac_scheduler.vhd
    #VHDL_SOURCES += $(WPWD)/../hdl/pbkdf2_input.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/wpa2_compare.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/gen_tenhex.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/wpa2_main.vhd
    #VHDL_SOURCES += $(WPWD)/../hdl/gen_ssid.vhd
    VHDL_SOURCES += $(WPWD)/../hdl/ztex_wrapper.vhd
    #For testing SHA1:
    #TOPLEVEL = sha1_scheduler
    #For testing HMAC:
    #TOPLEVEL = hmac_scheduler
    #For testing MK generation:
    #TOPLEVEL = gen_tenhex
    #For testing MK/PMK Comparison:
    #TOPLEVEL = wpa2_compare
    #For testing full WPA2:
    #TOPLEVEL = wpa2_main
    #For testing whole ZTEX board:
    TOPLEVEL = ztex_wrapper
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

#For testing SHA1:
#MODULE=test_sha1
#For testing HMAC:
#MODULE=test_hmac
#For testing PBKDF2:
#MODULE=test_wpa2
#For testing MK generation:
#MODULE=test_gentenhex
#For testing PMK comparison:
#MODULE=test_wpa2compare
#For testing the whoooole thing:
MODULE=test_ztex

CUSTOM_COMPILE_DEPS = hal

LD_LIBRARY_PATH := $(PWD)/../cosim:$(LD_LIBRARY_PATH)

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

.PHONY: hal
hal:
	-cd ../cosim && make

# Stuff below is useful for profiling
# Need grof2dot from https://github.com/jrfonseca/gprof2dot
test_profile.pstat: sim

callgraph.svg: test_profile.pstat
	$(GPROF2DOT)/gprof2dot.py -f pstats $< | dot -Tsvg -o $@

.PHONY: profile
profile:
	COCOTB_ENABLE_PROFILING=1 $(MAKE) callgraph.svg


clean::
	-rm -rf test_profile.pstat
	-rm -rf callgraph.svg
	-cd ../cosim && make clean
