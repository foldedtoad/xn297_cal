#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import json
from collections import OrderedDict


#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
def reverse(s): 
    str = "" 
    for i in s: 
        str = i + str
    return str

#------------------------------------------------------------------------------
# 
#------------------------------------------------------------------------------

class RF_Cal:

    EN_STBII_RX_2TX   = "?"
    BPF_CTRL_BW       = "?"
    BPF_CTRL_GAIN     = "?"
    PF_SEL            = "?"
    EN_PH             = "?"
    reserve1          = "?"
    RSSI_GAIN_CTR     = "?"
    reserve2          = "?"
    MIXL_GC           = "?"
    VCOBUF_IC         = "?"
    VCO_CT            = "?"
    CAL_VREF_SEL      = "?"
    DA_VREF_MB        = "?"
    DA_VREF_LB        = "?"
    DA_LPF_CTRL       = "?"
    SPI_CAL_EN        = "?"
    PREAMP_CTM        = "?"
    PA_BC             = "?"
    DA_LPF_BW         = "?"
    RX_CTM            = "?"
    RCCAL_EN          = "?"
    IB_BPF_TRIM       = "?"
    EN_VCO_CAL        = "?"
    PRE_BC            = "?"
    MIXL_BC           = "?"
    VCO_CODE_IN       = "?"
    LNA_GC            = "?"
    RCCAL_IN          = "?"
    VCO_BIAS          = "?"
    CPSEL             = "?"

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def __init__(self, dict_file, binary):

        self.binary = reverse(binary)
        self.dict_file = dict_file
        self.dict = None

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def modify_bitfield(self, key, value):

        RF_Cal.__dict__[key] = value

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def gather_bits(self, key):

        bits = ""
        bit_field_indices = self.dict[key]
        for bit in bit_field_indices:
            bits += self.binary[int(bit)]
        return bits

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def parse_parms(self):

        print("binary({0}): {1}".format(len(self.binary), self.binary))

        for key, value in self.dict.items():
            value = self.gather_bits(key)
            RF_Cal.__dict__[key] = value

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def print_parms(self):

        for key, value in self.dict.items():
            bits = RF_Cal.__dict__[key]
            print("{0:15} {1}".format(key, bits))

    #--------------------------------------------------------------------------
    # Compile a new binary (bit-array) from class variables.
    #--------------------------------------------------------------------------
    def compile_binary(self):

        self.binary = ""

        for key, value in self.dict.items():
            self.binary += RF_Cal.__dict__[key]

        #print("binary({0}): {1}".format(len(self.binary), self.binary))

    #--------------------------------------------------------------------------
    # Compose (regenerate) seven hex parms from binary string
    #--------------------------------------------------------------------------
    def compose_parms(self, binary):

        #print("binary({0}): {1}".format(len(binary), binary))

        parms_out = ""

        self.compile_binary()

        for n in range(0,7):
            bits = self.binary[(n*8)+0] + self.binary[(n*8)+1] + \
                   self.binary[(n*8)+2] + self.binary[(n*8)+3] + \
                   self.binary[(n*8)+4] + self.binary[(n*8)+5] + \
                   self.binary[(n*8)+6] + self.binary[(n*8)+7]

            parms_out +=  "0x" + format(int(bits,base=2), "X") + " "

        print("output: {0}".format(parms_out))

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def read_dictonary(self):

        # Access dictionary and insure dictionary is 'ordered'
        try:
            with open(self.dict_file) as json_dict:
                self.dict = json.load(json_dict, object_pairs_hook=OrderedDict)
        except:
            print "Couldn't load {0}".format(self.dict_file)
            return

        #print json.dumps(self.dict, indent=4)

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    def print_ruler(self):

        print("")
        print("                      1111111111222222222233333333334444444444555555")
        print("            01234567890123456789012345678901234567890123456789012345")
        print("            --------------------------------------------------------")
        print("Length({0}): {1}".format(len(self.binary), self.binary))
        print("")

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser()

    if len(sys.argv) != 3:
        print "wrong number of arguments: {0} of 2 args found".format(len(sys.argv) - 1)
        print "usage: rf_cal.py  <cal_parms_file> <json_dict_file>"
        sys.exit(1)

    parser.add_argument("cal_parms_file", help="Path to calibration parms file")
    parser.add_argument("json_dict_file", help="Path to JSON dictionary file")

    args = parser.parse_args()

    binary = ""

    #
    # Read in parameter file and create binary string from hex digits
    #
    try:
        with open(args.cal_parms_file, 'r') as cal_file:
            line = cal_file.readline()
            print("input:  {0}".format(line.strip()))

            hexnumerics = line.split()
            for hexnumeric in hexnumerics:
                binary += "{0:08b}".format(int(hexnumeric, base=16))
    except:
        pass

    #
    # Create instance of RF_Cal processor and run it.
    #
    rf_cal = RF_Cal(args.json_dict_file, binary)

    rf_cal.read_dictonary();
    rf_cal.parse_parms()
    rf_cal.print_parms()

    while 1: 
        print("--------------------------------------")
        key = raw_input("Enter field name > ").upper()
        if key == "QUIT":
            break
        bitnum = len(RF_Cal.__dict__[key])
        inbits = raw_input("Enter " + str(bitnum) + " bits > ")

        rf_cal.modify_bitfield(key, inbits)
        rf_cal.print_parms()

    rf_cal.compose_parms(rf_cal.binary)

    print "done"

    sys.exit(0)

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
if __name__ == "__main__":

    main()
