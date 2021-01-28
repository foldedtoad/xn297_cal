# xn297_rf_cal
XN297 (nRF24L01 clone) decoder for RF_CAL field

## Decoding the RF_CAL register for the XN297 2.4GHz radio
Below is an example of how to run this utility.  
There are two input files:
  * The text file which has its first line the 7 hexadecimal numerics for the RF_CAL params to be decoded.  
  Example: The "rf_cal.txt" file which contains the following.
  ```
  0xC9 0x9A 0xB0 0x61 0xBB 0xAB 0x9C
  ```
  * The JSON file which contains the JSON dictionary describing the bit-field layout of the RF_CAL register.
  Example: see the rf_cal.json file.


## Running the Utility
in this example running of the utility, the CPSEL bit-field is modified from a value of 0b00 to 0b11.  
After a field is modified, the whole RF_CAL register is echoed again, showing the newly changed field.
To exit edit process, type "quit", which will then display the complete 7 hexadecimal numeric parameter set.

```
xn297_rf_cal$ ./run.sh 
input:  0xC9 0x9A 0xB0 0x61 0xBB 0xAB 0x9C
binary(56): 00111001110101011101110110000110000011010101100110010011
EN_STBII_RX_2TX 1
BPF_CTRL_BW     1
BPF_CTRL_GAIN   0
PH_SEL          01
EN_PH           0
RESERVE1        0
RSSI_GAIN_CTR   11
RESERVE2        0
MIXL_GC         0
VCOBUF_IC       11
VCO_CT          01
CAL_VREF_SEL    0
DA_VREF_MB      101
DA_VREF_LB      100
DA_LPF_CTRL     0
SPI_CAL_EN      0
PREAMP_CTM      011
PA_BC           00
DA_LPF_BW       0
RX_CTM          01
RCCAL_EN        1
IB_BPF_TRIM     0
EN_VCO_CAL      1
PRE_BC          110
MIXL_BC         1
VCO_CODE_IN     1101
LNA_GC          01
RCCAL_IN        011100
VCO_BIAS        111
CPSEL           00
--------------------------------------
Enter field name > CPSEL
Enter 2 bits > 11
EN_STBII_RX_2TX 1
BPF_CTRL_BW     1
BPF_CTRL_GAIN   0
PH_SEL          01
EN_PH           0
RESERVE1        0
RSSI_GAIN_CTR   11
RESERVE2        0
MIXL_GC         0
VCOBUF_IC       11
VCO_CT          01
CAL_VREF_SEL    0
DA_VREF_MB      101
DA_VREF_LB      100
DA_LPF_CTRL     0
SPI_CAL_EN      0
PREAMP_CTM      011
PA_BC           00
DA_LPF_BW       0
RX_CTM          01
RCCAL_EN        1
IB_BPF_TRIM     0
EN_VCO_CAL      1
PRE_BC          110
MIXL_BC         1
VCO_CODE_IN     1101
LNA_GC          01
RCCAL_IN        011100
VCO_BIAS        111
CPSEL           11
--------------------------------------
Enter field name > quit
output: 0xC9 0x9A 0xB0 0x61 0xBB 0xAB 0x9F 
done
```

