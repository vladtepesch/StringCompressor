#include <stdint.h>


static const uint8_t s_cdata[][2] = 
{{2, 65},
 {251, 32},
 {4, 3},
 {53, 52},
 {6, 5},
 {46, 45},
 {8, 7},
 {37, 36},
 {10, 9},
 {30, 29},
 {12, 11},
 {24, 23},
 {14, 13},
 {148, 147},
 {144, 143},
 {94, 210},
 {113, 209},
 {46, 60},
 {107, 47},
 {122, 214},
 {70, 213},
 {72, 33},
 {54, 82},
 {220, 219},
 {218, 217},
 {86, 78},
 {51, 52},
 {62, 84},
 {93, 91},
 {227, 226},
 {224, 159},
 {41, 225},
 {87, 53},
 {40, 69},
 {119, 121},
 {255, 73},
 {235, 170},
 {167, 166},
 {50, 233},
 {79, 232},
 {48, 77},
 {58, 68},
 {65, 236},
 {67, 98},
 {49, 118},
 {243, 242},
 {240, 175},
 {45, 241},
 {80, 103},
 {104, 109},
 {102, 100},
 {99, 112},
 {250, 249},
 {247, 182},
 {114, 248},
 {117, 10},
 {97, 115},
 {110, 105},
 {108, 111},
 {116, 101}};

CompressionData CompD ={s_cdata};


const uint8_t compressed[] = 
{2, 145, 141, 46, 93, 103, 31, 170, 157, 85, 92, 101, 22, 72, 30, 5, 255, 255, 254, 170, 189, 137, 2, 128, 191, 255, 255, 
205, 83, 221, 50, 213, 134, 164, 8, 5, 255, 255, 255, 92, 176, 214, 85, 192, 115, 222, 186, 195, 89, 87, 214, 215, 54, 152, 245, 153, 151, 105, 247, 133, 170, 175, 11, 92, 112, 184, 205, 238, 53, 17, 124, 120, 48, 176, 86, 178, 174, 133, 233, 252, 110, 99, 93, 20, 214, 100, 4, 9, 237, 68, 53, 17, 63, 255, 255, 255, 142, 23, 25, 143, 102, 53, 209, 77, 98, 252, 45, 
120, 242, 245, 92, 105, 169, 255, 255, 255, 252, 112, 184, 204, 86, 99, 93, 20, 214, 47, 194, 215, 61, 16, 63, 48, 60, 198, 84, 164, 128, 129, 50, 134, 53, 209, 77, 98, 72, 11, 255, 255, 254, 23, 114, 195, 89, 87, 200, 8, 19, 194, 199, 189, 117, 134, 178, 175, 156, 170, 0, 69, 113, 129, 249, 141, 67, 165, 80, 82, 72, 23, 255, 255, 252, 93, 235, 172, 53, 149, 124, 
128, 129, 52, 144, 64, 255, 255, 255, 175, 102, 66, 170, 230, 44, 202, 173, 167, 100, 4, 9, 230, 49, 166, 0, 201, 255, 255, 255, 252, 127, 43, 21, 149, 208, 199, 131, 90, 234, 233, 180, 238, 22, 185, 170, 171, 152, 179, 42, 184, 89, 105, 158, 241, 250, 125, 95, 133, 174, 184, 122, 242, 151, 198, 49, 166, 0, 216, 88, 120, 14, 19, 44, 6, 10, 211, 255, 255, 255, 255, 249, 244, 229, 144, 200, 45, 130, 114, 129, 216, 240, 28, 38, 88, 13, 128, 248, 160, 16, 39, 40, 29, 143, 9, 150, 3, 113, 229, 234, 179, 149, 64, 8, 174, 48, 61, 36, 3, 193, 163, 224, 207, 255, 245, 236, 227, 77, 218, 118, 64, 64, 159, 30, 94, 171, 11, 31, 78, 89, 12, 152, 240, 144, 144, 144, 82, 127, 255, 255, 255, 31, 202, 225, 107, 198, 155, 143, 172, 196, 93, 167, 112, 181, 204, 106, 29, 42, 188, 26, 8, 22, 30, 18, 20, 8, 6, 39, 255, 255, 255, 255, 243, 233, 203, 33, 144, 91, 30, 18, 18, 18, 202, 7, 97, 96, 231, 194, 216, 160, 16, 39, 53, 85, 115, 22, 101, 80, 86, 60, 3, 1, 64, 108, 128, 129, 50, 134, 7, 152, 203, 164, 135, 15, 255, 255, 250, 246, 112, 181, 205, 14, 47, 152, 210, 230, 172, 171, 143, 172, 196, 92, 44, 
62, 3, 198, 155, 146, 241, 250, 191, 11, 92, 244, 64, 252, 192, 243, 25, 66, 147, 255, 255, 255, 251, 178, 184, 90, 224, 180, 23, 27, 85, 180, 238, 22, 185, 15, 118, 60, 80, 33, 63, 255, 255, 255, 143, 229, 112, 181, 205, 14, 47, 143, 172, 196, 92, 26, 36, 44, 60, 36, 40, 16, 12, 74, 69, 222, 75, 226, 204, 195, 68, 99, 26, 232, 166, 177, 34, 224, 209, 192, 207, 255, 253, 85, 99, 215, 225, 107, 177, 164, 188, 205, 148, 126, 179, 105, 218, 204, 102, 123, 201, 124, 89, 152, 104, 130, 136, 123, 151, 79, 255, 255, 255, 227, 178, 183, 157, 174, 109, 49, 231, 62, 159, 185, 187, 81, 13, 68, 195, 158, 198, 99, 110, 77, 117, 82, 210, 159, 141, 68, 225, 107, 167, 255, 255, 255, 255, 245, 222, 75, 150, 102, 245, 245, 143, 62, 159, 198, 236, 122, 243, 105, 218, 239, 37, 203, 49, 126, 55, 106, 33, 168, 153, 181, 79, 105, 239, 49, 102, 48, 61, 63, 255, 255, 255, 255, 133, 138, 40, 29, 131, 194, 249, 141, 46, 93, 103, 30, 20, 159, 255, 255, 255, 213, 98, 20, 229, 245, 157, 143, 172, 196, 92, 229, 52, 190, 36, 80, 160, 144, 148, 139, 184, 26, 56, 25, 255, 254, 170, 177, 235, 240, 181, 216, 210, 94, 102, 202, 63, 89, 180, 238, 22, 185, 239, 37, 241, 102, 97, 162, 10, 32, 52, 23, 185, 63, 255, 255, 255, 187, 43, 133, 174, 11, 65, 113, 181, 91, 78, 225, 107, 144, 247, 99, 197, 6, 28, 39, 255, 255, 255, 241, 217, 91, 206, 215, 54, 152, 243, 
159, 79, 220, 221, 168, 134, 162, 97, 207, 99, 49, 183, 38, 186, 169, 105, 79, 198, 162, 112, 181, 211, 255, 255, 255, 255, 250, 239, 37, 203, 51, 122, 250, 199, 159, 79, 227, 118, 61, 121, 180, 237, 119, 146, 229, 152, 191, 27, 181, 16, 212, 76, 218, 167, 180, 247, 152, 179, 24, 30, 159, 255, 255, 255, 255, 194, 197, 20, 14, 193, 225, 124, 198, 151, 46, 179, 143, 10, 79, 255, 255, 255, 234, 177, 10, 114, 248, 150, 243, 182, 52, 59, 106, 177, 237, 231, 101, 158, 73, 100, 139, 184, 245, 255, 255, 245, 236, 95, 133, 174, 46, 242, 95, 22, 102, 26, 33, 63, 255, 255, 255, 187, 43, 133, 174, 11, 65, 113, 181, 91, 78, 225, 107, 144, 247, 99, 197, 6, 28, 39, 255, 255, 255, 243, 242, 179, 222, 170, 100, 123, 93, 180, 236, 52, 70, 107, 221, 167, 255, 255, 255, 255, 240, 209, 108, 53, 198, 162, 105, 255, 255, 255, 255, 252, 64, 182, 33, 16, 212, 68, 255, 255, 255, 254, 190, 86, 188, 90, 93, 167, 100, 61, 201, 255, 255, 255, 255, 252, 72, 91, 12, 76, 104, 118, 243, 177, 8, 
134, 162, 109, 86, 66, 24, 196, 27, 136, 56, 237, 231, 111, 113, 168, 137, 255, 255, 255, 255, 252, 120, 91, 2, 158, 73, 109, 231, 98, 17, 13, 68, 218, 172, 132, 49, 136, 55, 16, 237, 231, 111, 113, 168, 137, 72, 231, 44, 198, 147, 134, 184, 212, 76, 99, 93, 20, 214, 36, 112, 95, 255, 255, 240, 187, 150, 26, 202, 190, 56, 92, 98, 71, 11, 255, 255, 254, 46, 245, 214, 26, 202, 190, 56, 92, 98, 71, 1, 229, 255, 255, 252, 49, 78, 178, 153, 23, 225, 107, 143, 181, 145, 98, 110, 170, 117, 
85, 113, 151, 57, 170, 199, 11, 140, 79, 255, 255, 255, 229, 242, 177, 225, 111, 5, 12, 24, 159, 255, 255, 255, 255, 197, 
11, 125, 12, 120, 149, 78, 89, 154, 169, 222, 159, 255, 255, 255, 255, 255, 192, 60, 20, 48, 103, 239, 59, 93, 238, 37, 151, 174, 62, 159, 137, 213, 151, 66, 169, 122, 232, 159, 255, 255, 255, 255, 255, 192, 60, 20, 24, 176, 24, 176, 80, 246, 243, 179, 222, 113, 213, 78, 49, 235, 51, 19, 171, 46, 133, 82, 245, 209, 63, 255, 255, 255, 255, 130, 5, 188, 120, 2, 30, 
5, 39, 255, 255, 255, 255, 240, 72, 183, 138, 0, 130, 64, 236, 21, 158, 245, 204, 107, 157, 76, 148, 252, 112, 30, 23, 2, 
20, 64, 104, 45, 63, 255, 255, 255, 255, 132, 139, 120, 160, 8, 36, 14, 193, 88, 115, 225, 108, 197, 141, 88, 199, 198, 171, 49, 174, 57, 228, 161, 84, 254, 55, 28, 7, 133, 192, 133, 16, 247, 36, 115, 139, 131, 71, 3, 63, 255, 85, 88, 245, 248, 90, 235, 57, 102, 52, 156, 125, 102, 34, 237, 118, 67, 221, 185, 63, 255, 255, 255, 187, 43, 5, 160, 184, 218, 173, 167, 
97, 174, 53, 19, 53, 238, 199, 138, 4, 248, 97, 80, 241, 65, 56, 113, 106, 171, 132, 239, 95, 133, 174, 247, 74, 167, 44, 
206, 82, 230, 213, 45, 16, 171, 175, 92, 187, 84, 159, 255, 255, 255, 203, 229, 99, 80, 246, 31, 172, 63, 84, 177, 55, 104, 253, 86, 40, 4, 95, 47, 86, 93, 10, 165, 235, 162, 248, 88, 184, 6, 24, 122, 18, 20, 159, 255, 255, 255, 199, 101, 111, 
59, 92, 218, 99, 206, 125, 63, 115, 118, 162, 26, 137, 135, 61, 140, 198, 220, 154, 234, 165, 165, 63, 26, 137, 194, 215, 
79, 255, 255, 255, 255, 235, 188, 151, 44, 205, 235, 235, 30, 125, 63, 141, 216, 245, 230, 211, 181, 222, 75, 150, 98, 252, 110, 212, 67, 81, 51, 106, 158, 211, 222, 98, 204, 96, 122, 127, 255, 255, 255, 255, 11, 20, 80, 59, 7, 133, 243, 26, 92, 186, 206, 60, 41, 41, 34, 169, 237, 61, 230, 98, 17, 13, 68, 198, 53, 209, 77, 98, 65, 227, 159, 255, 255, 235, 216, 191, 11, 93, 117, 139, 154, 199, 184, 157, 238, 149, 67, 235, 51, 57, 170, 205, 170, 123, 79, 121, 139, 51, 89, 203, 49, 164, 229, 234, 203, 161, 84, 189, 116, 93, 63, 255, 255, 255, 191, 43, 123, 165, 80, 250, 204, 222, 236, 186, 233, 7, 139, 191, 255, 255, 215, 177, 126, 22, 186, 235, 23, 53, 143, 113, 59, 221, 42, 135, 214, 102, 115, 85, 155, 84, 246, 158, 243, 22, 102, 123, 201, 124, 89, 153, 122, 178, 232, 85, 47, 93, 23, 79, 255, 255, 255, 239, 202, 222, 233, 84, 62, 179, 55, 187, 46, 186, 65, 226, 255, 255, 255, 175, 26, 106, 252, 45, 117, 145, 26, 93, 104, 243, 53, 235, 143, 123, 137, 218, 118, 94, 172, 186, 21, 75, 215, 76, 125, 102, 34, 174, 159, 255, 255, 255, 214, 113, 250, 170, 246, 47, 194, 215, 94, 178, 153, 30, 215, 97, 197, 150, 156, 110, 189, 113, 233};


static const char uncompressed[] = R"(
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
)";
