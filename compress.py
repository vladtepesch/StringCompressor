from functools import reduce
import pprint
import math

strDataOrg = r'''The bytes type in Python is immutable and stores a sequence of values 
      ranging from 0-255 (8-bits). You can get the value of a single 
      byte by using an index like an array, but the values can not be modified.
      '''

strDataOrg = r'''
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

maxTree = 60

hist = {}

strData = bytes(strDataOrg, 'ascii')

for c in strData:
    if chr(c) in hist:
        hist[chr(c)]['n'] =  hist[chr(c)]['n'] + 1
    else:
        hist[chr(c)] = {'n':1, 'bl':c.bit_length()}

histS = sorted(hist.items(), key = lambda x: x[1]['n'], reverse=True)
weight = reduce(lambda a,b:a+b[1]['n'], histS, 0)

for h in histS:
    print(h[0],': ', h[1] )

print(len(histS), 'distinct symbols')

regSyms  = histS[0:maxTree]
regSymsW = reduce(lambda a,b:a+b[1]['n'], regSyms, 0)
restSyms  = histS[maxTree:]
restSymsW = reduce(lambda a,b:a+b[1]['n'], restSyms, 0)

print()
print("reg: ", regSyms)
print("sum: ", regSymsW)

print("rest: ", restSyms)
print("sum: ", restSymsW)
if len(restSyms) > 0:
    syms = regSyms + [('rest',{'n':restSymsW})]
else:
    syms = regSyms
    
syms = sorted(syms, key = lambda x: x[1]['n'], reverse=True)

print("syms: ", syms)
print("sum: ", weight)

#x.bit_length()    

top = {
    'id':0,
    'name':'TOP',
    'P':None,
    'syms': syms,
    'w': weight,
    'code':''
}
nodes = {top['name']:top}

stack = [top]

gStr = ''

symbolTable = {}

decompressData = []
def extendList(l, n, pad=0):
    if len(l) < n:
        l.extend([pad] * (n - len(l)))
noN = 1
while (len(stack) > 0):
    i = stack.pop()
    wh = i['w']/2
    sp = 0
    spS = 0
    while spS < wh:
        spS = spS + i['syms'][sp][1]['n']
        sp = sp + 1
    
    a = {
        'P':i['name'],
        'w': spS,
        'syms':i['syms'][:sp],
        'code':i['code']+'1',
    }
    b = {
        'P':i['name'],
        'r':False,
        'w': i['w']-spS,
        'syms':i['syms'][sp:],
        'code':i['code']+'0',
    }
    i['a'] = a
    i['aleaf'] = len(a['syms'])<=1
    i['b'] = b
    i['bleaf'] = len(b['syms'])<=1
    #i['refId'] = str(i['id'])+'_' + ('1' if i['bleaf'] else '0') + ('1' if i['aleaf'] else '0')
    i['refId'] =  i['id'] | (0x80 if i['bleaf'] else 0) | (0x40 if i['aleaf'] else 0)
    if not i['aleaf']:
        a['name'] = 'N'+str(noN)
        a['id'] = noN
        noN = noN + 1
        stack.append(a)
        #print('added a: ', a)
    else:        
        a['name'] = '[' + a['syms'][0][0] + ']'
        symbolTable[ a['syms'][0][0]] = a
    if not i['bleaf']:
        b['name'] = 'N'+str(noN)
        b['id'] =  noN
        noN = noN + 1
        stack.append(b)
        #print('added b: ', b)
    else:
        b['name'] = '[' + b['syms'][0][0] + ']'
        symbolTable[ b['syms'][0][0]] = b
        
    #aLinkId = 
    nodes[a['name']] = a
    nodes[b['name']] = b

    extendList(decompressData, i['id']+1, [])
    #decompressData[i['id'] ] = [ b['id'] if not i['bleaf'] else '[' + b['syms'][0][0] + ']', 
    #                             a['id'] if not i['aleaf'] else '[' + a['syms'][0][0] + ']' ]
    decompressData[i['id'] ] = [b['name'], a['name']]
    gStr = gStr +  '"' + i['code'] +'\\n'+ i['name'] + '" -> "'  + a['code'] +'\\n'+ a['name'] + '"' + ";\n"
    gStr = gStr +  '"' + i['code'] +'\\n'+ i['name'] + '" -> "'  + b['code'] +'\\n'+ b['name'] + '"' + ";\n"

 #   sys.exit()

print(gStr)
pprint.pprint(symbolTable)
#pprint.pprint(decompressData)
#
decompressData2 = []
for ni in nodes.items():
    i = ni[1]
    if 'id' in i:
        extendList(decompressData2, i['id']+1, [])
        decompressData2[i['id'] ] = [i['b']['refId'] if 'refId' in i['b'] else (ord(i['b']['syms'][0][0]) if i['b']['syms'][0][0] != 'rest' else 255), 
                                     i['a']['refId'] if 'refId' in i['a'] else (ord(i['a']['syms'][0][0]) if i['a']['syms'][0][0] != 'rest' else 255) ]

print(pprint.pformat(decompressData2).replace('[', '{').replace(']', '}'))


## compress
compressed = ''
for c in strData:
    if chr(c) in symbolTable:
        compressed = compressed + ' ' + symbolTable[chr(c)]['code']
    else:
        compressed = compressed + ' ' + symbolTable['rest']['code'] + '_' + "{0:08b}".format(c)

print(compressed)
compressed = compressed.replace('_', '').replace(' ', '')

# add 1 start bit and right align with padded 0 at front (and throw this away in decoder)
# --> we always end at byte boundaries so there is no ambiguity in decoder
compressed = '1' + compressed
if len(compressed)%8 != 0:
  compressed =  (8-len(compressed)%8)*'0'  + compressed
##



decompDataSize = len(decompressData2) * 2

print("cleaned: ", math.ceil(len(compressed)/8),'Bytes (',len(compressed), 'bits) of ',len(strData) , 'Bytes -->', round(100/8 * len(compressed)/len(strData),2), '%')
print("incl decomp data: ", math.ceil(decompDataSize + len(compressed)/8),'Bytes (',decompDataSize * 8 + len(compressed), 'bits) of ',len(strData) , 'Bytes -->', round(100/8 * (len(compressed)+decompDataSize*8)/len(strData),2), '%')
print(compressed)
#pprint.pprint(top)


compressedBin = []
compressedStream = compressed
while len(compressedStream) > 0:
    ch = compressedStream[0:8]
    ch = ch.ljust(8, '0')
    compressedStream = compressedStream[8:]
    compressedBin.append(int(ch,2))

print(compressedBin)

##  decompress
decompressData  = decompressData2
compressedStream = compressed
decompressed = ''

# throw away padded 0
while compressedStream[0] != '1':
  compressedStream = compressedStream[1:]

# throw away start bit
compressedStream = compressedStream[1:]

while len(compressedStream) > 0:
    s = 0
    nextIsEnd = [False, False]
    finishedSymbol = False
    
    while not finishedSymbol:
        bit = 0 if compressedStream[0]=='0' else 1
#        print("next bit: ", bit)
        compressedStream = compressedStream[1:]
        nId = decompressData[s][bit]
        if nextIsEnd[bit]:
#            print("  is end: ")
            if nId==255:
#                print("    rest - reading addional bits ")
                ch = compressedStream[0:8]
                compressedStream = compressedStream[8:]
                sym = chr(int(ch,2))
            else:
                sym = chr(nId)
#            print("  symbol: ", ord(sym), " '", sym, "'")
            decompressed = decompressed + sym
            finishedSymbol = True
        else:
            nextIsEnd[0] = nId & 0x80 != 0
            nextIsEnd[1] = nId & 0x40 != 0
            s = nId & 0x3F
#            print("  nextNodeId: ", s, " " ,nextIsEnd )

    
  #  sys.exit()

#print(decompressed)
print(decompressed == strDataOrg)

##



#
# [[2, 1],          [['2_00', '1_00'],
#  [146, 209],       ['18_10', '17_11'],
#  [4, 3],           ['4_00', '3_00'],
#  [142, 141],       ['14_10', '13_10'],
#  [6, 5],           ['6_00', '5_00'],
#  [204, 203],       ['12_11', '11_11'],
#  [136, 135],       ['8_10', '7_10'],
#  [100, 202],       ['[d]', '10_11'],
#  [118, 201],       ['[v]', '9_11'],
#  [99, 102],        ['[c]', '[f]'],
#  [109, 104],       ['[m]', '[h]'],
#  [108, 121],       ['[l]', '[y]'],
#  [103, 114],       ['[g]', '[r]'],
#  [115, 208],       ['[s]', '16_11'],
#  [98, 207],        ['[b]', '15_11'],
#  [117, 111],       ['[u]', '[o]'],
#  [105, 116],       ['[i]', '[t]'],
#  [255, 32],        ['[rest]', '[ ]'],
#  [97, 211],        ['[a]', '19_11'],
#  [110, 101]]       ['[n]', '[e]']]
# 





















