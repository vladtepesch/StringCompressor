from functools import reduce
from tabnanny import verbose
from bitarray import bitarray
from bitarray.util import ba2base
from bitarray.util import ba2int
import pprint
import math


from StringCompressor import StringCompressor

testData=[
  {  
     'treeSize': 5,
     'byteDataOrg' : bytes([0,0,0,0,1,20,1,1,255,255,50,50,50,0,0,1,20,1,255,20,1,0,0,1,50,50])
  },
  {  
     'treeSize': 5,
     'strDataOrg' : r'''The bytes type in Python is immutable and stores a sequence of values 
      ranging from 0-255 (8-bits). You can get the value of a single 
      byte by using an index like an array, but the values can not be modified.
      '''
  },
  {  
     'treeSize': 5,
     'strDataOrg' : r'abaaaabaaaaabbaacXaaaaaaaaKJabbcca'
  },  
  {  
     'treeSize': 5,
     'strDataOrg' : r'abbaaaaabbaacXKJabbcca'
  },
  {  
     'treeSize': 20,
     'strDataOrg' : r'''
Command reference:
R!           reset
H!           print help
F!           enables/disables a special mode there the ADC inputs 1,2 are used to control PWM output
               ADC 1 controls the timer top
               ADC 2 controls the duty cycle

PWM-Control
PE           Enables PWM (disables frequency counter)
PD           Disables PWM
PPv          set Prescaler of PWM clock
               v - 2 - exponent of the prescaler that divedes the system Clock (16Mhz) 
                   default: 4 -> 16Mhz / 2^4 -> 1Mhz timer frequency
PT[v]        set top of PWM timer (default 1000)
               v - the top value of the counter  [3:1023]
                   default: 1000 -> (with 2^4 prescaler) 1kHz PWM-Cycle 
Pnv          set the pwm compare value (v/top gives the duty cycle)
               n - the Number of the Pin 1-3
               v - the pwm value [0:1023]

Digital IO Control
D[A]         reads the logic level of all digital IO-Pins
               A - if specified no output will be generated but the 
                   signal is added to list of signals to output periodically
                   (--> TE command)
               returns an value from 0-255
Dn[A]        reads the logic level of the digital IO-PIN n
               n - the Number of the Pin 1-8
               A - if specified no output will be generated but the 
                   signal is added to list of signals to output periodically
                   (--> TE command)
               returns 0 if low or 1 if high
Dnds         sets the Digital IO
               n - the Number of the Pin 1-8
               d - direction of IO pin 
                   I: Input 
                   O: Output
               s - state of Pin
                   0: Low if Output or Pullup Off if input
                   1: High if Output or Pullup On if input

Analog Input Control
AE           Enables ADC
AD           Disables ADC
ARm          Selects the voltage reference for ADC
               m - 1:  VCC
                   2:  external ref  
                       < VCC   if single ended Measurement
                       < VXX-1 if differncial Measurement
                   3:  1.1V
                   4:  2.56 V disconnected AREF-PIN
                   5:  2.56 V with capacitor configured to AREF-Pin
Anm[A]       reads the analog value on Pin n
               n - Number of Input pin 1-4  *1-5 where 5 is the internal temperature sensor
               m - build average over 2^m measurements (m<=5)
               A - if specified no output will be generated but the 
                   signal is added to list of signals to output periodically
                   (--> TE command)

Periodic Output Control
TAi          sets the sampling interval for periodical analog measurements
               i - interval in ms
TDi          sets the sampling interval for periodical digital measurements
               i - interval in ms
TD           stops the automatic sending of measurement values
               and resets the selection what to send
'''
  }
]

td = testData[0]
isBinData = "byteDataOrg" in td

maxTree = td['treeSize']

compressor = StringCompressor(maxTree, verbose=True, treeShanon=False)
if isBinData:
  compressor.trainFromBytes(td["byteDataOrg"])
else:
  compressor.trainFromString(td["strDataOrg"])
compressor.printDotGraph()
compressor.printMermaidGraph()


print(pprint.pformat(compressor.decompressData).replace('[', '{').replace(']', '}'))

if isBinData:
  compressed = compressor.compressBytes(td["byteDataOrg"])
  orgLen = len(td["byteDataOrg"])
else:
  compressed = compressor.compressString(td["strDataOrg"])
  orgLen = len(td["strDataOrg"])

compLen = len(compressed)
decompDataSize = len(compressor.decompressData) * 2

print("compressed: ", math.ceil(compLen),'Bytes (',compLen*8, 'bits) of ',orgLen , 'Bytes -->', round(100 * compLen/orgLen,2), '%')
print("incl decomp data (",decompDataSize,"B): ", math.ceil(decompDataSize + compLen),'Bytes (',decompDataSize * 8 + compLen*8, 'bits) of ',orgLen , 'Bytes -->', round(100 * (compLen+decompDataSize)/orgLen,2), '%')
#print(compressed)
#pprint.pprint(top)

# output bitarray as byte array
print(list(compressed))
#compressedBa = bitarray()
#compressedBa.frombytes(compressed)
#pprint.pprint(compressedBa)
if isBinData:
  decompressed = compressor.decompress(compressed)
  print(decompressed)
  print("decompressed equals original:", decompressed == td["byteDataOrg"])
else:
  decompressed = compressor.decompressString(compressed)
  print(decompressed)
  print("decompressed equals original:", decompressed == td["strDataOrg"])


compressor2 = StringCompressor()
compressor2.loadDecompressData(compressor.decompressData)
#pprint.pprint(reNodes)
#printDotGraph(reNodes)
if isBinData:
  comp2 = compressor2.compressBytes(td["byteDataOrg"])
  print("compressed equals:", comp2 == compressed)
  decompressed2 = compressor2.decompress(comp2)
  print("decompressed2 equals original:", decompressed == td["byteDataOrg"])
else:
  comp2 = compressor2.compressString(td["strDataOrg"])
  print("compressed equals:", comp2 == compressed)
  decompressed2 = compressor2.decompressString(comp2)
  print("decompressed2 equals original:", decompressed == td["strDataOrg"])





















