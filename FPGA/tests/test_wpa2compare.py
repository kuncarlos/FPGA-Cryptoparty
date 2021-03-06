#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#                                test_wpa2compare.py 
#    Tests for calculating PMK from MK and comparing - Modify Makefile to run 
#    Copyright (C) 2016  Jarrett Rainier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.result import TestFailure
from cocotb.log import SimLog
from cocotb.wavedrom import Wavedrom
import random
_debug = False

@cocotb.coroutine
def load_random_data(dut, log, mockObject, bytes):
    secret = ''
    value = ''
    if dut != None:
        dut.load_secret_i <= 1
    
    for i in range(bytes):
        inputSecret = random.randint(ord('A'), ord('z'))
        inputValue = random.randint(ord('A'), ord('z'))
        secret = secret + chr(inputSecret)
        value = value + chr(inputValue)
        if _debug == True:
            log.info(str(i) + " - {} - ".format(int(str(dut.pbuffer1.i), 2)) + " {}".format(convert_hex(dut.pbuffer1.test_word_2)) + " {}".format(convert_hex(dut.pbuffer1.test_word_3)))

    if mockObject != None:
        mockObject.load(secret, value)
        
    if dut != None:
        for i in range(bytes / 4):
            dut.secret_i <= secret[(i * 4):((i * 4) + 3)]
            yield RisingEdge(dut.clk_i)
        if bytes % 4 > 0:
            dut.secret_i <= secret[-1 * (bytes % 4):]
            yield RisingEdge(dut.clk_i)
        dut.load_secret_i <= 0
        
        
        
@cocotb.coroutine
def reset(dut):
    dut.rst_i <= 1
    yield RisingEdge(dut.clk_i)
    dut.rst_i <= 0
    #yield RisingEdge(dut.clk_i)
    #log.info("Reset!")


@cocotb.coroutine
def load_data(dut):
    dut.rst_i <= 1
    yield RisingEdge(dut.clk_i)
    dut.rst_i <= 0

@cocotb.test()
def A_gen_data_test(dut):
    """
    Tests that gen_tenhex generates sane values
    """
    log = SimLog("cocotb.%s" % dut._name)
    cocotb.fork(Clock(dut.clk_i, 10000).start())
    
    outStr = ''
    
    yield reset(dut)
    yield RisingEdge(dut.clk_i)
        
    for x in xrange(0xff):
        complete = int(dut.main1.gen1.complete_o.value)
        if complete != 0:
            raise TestFailure("Premature completion")
        
        outStr = '{:x}'.format(int(dut.main1.gen1.mk_test9.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test8.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test7.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test6.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test5.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test4.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test3.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test2.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test1.value)) + \
            '{:x}'.format(int(dut.main1.gen1.mk_test0.value))
       
        
        yield RisingEdge(dut.clk_i)
        
    if outStr != "00000000fe":
        raise TestFailure("Wrong loaded values!")
    else:
        log.info("Ok!")

@cocotb.test()
def B_compare_data_test(dut):
    """
    Tests that generated data gets compared against test values
    """
    log = SimLog("cocotb.%s" % dut._name)
    cocotb.fork(Clock(dut.clk_i, 10000).start())
    
    outStr = ''
    
    yield reset(dut)
    yield RisingEdge(dut.clk_i)
        
    for x in xrange(0x90):
        complete = int(dut.main1.comp_complete)
        
        outStr = str(x) + ' - ' + str(int(dut.main1.i.value)) + ' - ' + str(complete) + ' - ' + \
            '{:x}'.format(int(dut.main1.comp1.mk_test_comp.value)) + ": " + \
            '{:x}'.format(int(dut.main1.comp1.mk_test9.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test8.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test7.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test6.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test5.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test4.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test3.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test2.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test1.value)) + \
            '{:x}'.format(int(dut.main1.comp1.mk_test0.value))
            
        if complete == 1:
            break
        
        yield RisingEdge(dut.clk_i)
        
    if complete == 0:
        raise TestFailure("Comparison never reached")
    else:
        log.info("Ok!")
        
        

#@cocotb.test()
def Y_populate_prf_test(dut):
    """
    Pushes PRF data with known values
    """
    log = SimLog("cocotb.%s" % dut._name)
    cocotb.fork(Clock(dut.clk_i, 10000).start())
    
    objSha = Sha1Model()
    objHmac = HmacModel(objSha)
    objPrf = PrfModel(objHmac)
    
    #pmk = '9051ba43660caec7a909fbbe6b91e4685f1457b5a2e23660d728afbd2c7abfba'
    #apMac = '001dd0f694b0'
    #cMac = '489d2477179a'
    #apNonce = '87f2718bad169e4987c94255395e054bcaf77c8d791698bf03dc85ed3c90832a'
    #cNonce = '143fbb4333341f36e17667f88aa02c5230ab82c508cc4bd5947dd7e50475ad36'
    
    pmk = '01b809f9ab2fb5dc47984f52fb2d112e13d84ccb6b86d4a7193ec5299f851c48'
    apMac = '001e2ae0bdd0'
    cMac = 'cc08e0620bc8'
    apNonce = '61c9a3f5cdcdf5fae5fd760836b8008c863aa2317022c7a202434554fb38452b'
    cNonce = '60eff10088077f8b03a0e2fc2fc37e1fe1f30f9f7cfbcfb2826f26f3379c4318'
    
    ptk = objPrf.PRF(pmk, apMac, cMac, apNonce, cNonce)
    
    print "Goal  : bf49a95f0494f44427162f38696ef8b6"
    print "Result: " + ptk
    
    data = "0103005ffe0109002000000000000000010000000000000000000000000000000000000" + \
        "00000000000000000000000000000000000000000000000000000000000000000000000000" + \
        "00000000000000000000000000000000000000000000000000000"
    

    mic = objPrf.MIC(ptk, data)
    
    print "Goal  : 45282522bc6707d6a70a0317a3ed48f0"
    print "Result: " + mic
    
    yield reset(dut)
    #yield load_data(dut, log, mockSha1, 16)

        
        
        
        
def convert_hex(input):
    input = str(input)
    replaceCount = []
    while 'UUUU' in input: 
        replaceCount.append(input.find('UUUU') / 4)
        input = input.replace('UUUU', '1111', 1)
    
    try:
        output = list("{:x}".format(int(str(input), 2)))
    except:
        output = list("{}".format(str(input)))
    
    
    for x in replaceCount:
        if len(output) > x:
            output[x] = 'U'
        else:
            output.append('U')
        
    return "".join(output)
    
    
    
