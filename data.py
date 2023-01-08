{
  # global default config that can be overridden from within any compression group
  # by just redefining the value within 
  # (of course not applicable for includes and file header)
  'config' : {
    # weather to prepend a file header with no-edit note 
    # (default: False)
    'doNotEditFileHeader': True,

    # list of additional include directives 
    # (default: [])
    'includes' : ['<stdint.h>'],

    # how the data variables get declared 
    # (default: static const uint8_t) 
    'declType' : 'static const uint8_t',


    # if the original Data should be prepend to the compressed data as comment
    # (default: False)
    'originalDataAsComment' : True,

    # prepend a comment with compression size to the compressed data 
    # (default: False)
    'compressionStatsAsComment' : True,

  },

  # list of different compression groups
  # each group gets its own compression tree (decompression data)
  # but may contain multiple independent data to compress 
  'data' : [

    # the 'name' becomes the variable name of the compression data
    # the 'data' member contains key-value pairs where the key is the name 
    # of the variable holding the compressed data and the value the data to compress
    # the compression data is build upon all data values in the group
    {
      "name" : "c_cdhelptext",
      "maxTree": 10,
      "data":{
        "s_test1":"hallo",
        "s_test2":"hallohallohallohallohallohallohallohallohallohallohallohallohallo",
        "s_test3":"hallo123"
      }
    },
    {
      "name" : "c_cdLoremIpsum",
      "maxTree": 10,
      "data":{
        "s_lorem1":"LoremIpsum",
        "s_lorem2":"LoremIpsumLoremIpsumLoremIpsumLoremIpsumLoremIpsumLoremIpsum",
        "s_lorem3":"LoremIpsum\nLoremIpsum\nLoremIpsum\n    LoremIpsum\n    LoremIpsum"
      }
    },
    {
      "name" : "c_cdTinyControlHelp",
      "maxTree":30,
     # 'originalDataAsComment' : False,

      "data":{
        "s_tctrlHelp":  r'''
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
               v - 2 - exponent of the prescaler that divides the system Clock (16Mhz) 
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
                       < VXX-1 if differential Measurement
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
    }
]
}