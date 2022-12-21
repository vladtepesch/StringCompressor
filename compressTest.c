#include "StringDecompressor.h"

#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>


#include "text.h"



/*

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
*/

#include <assert.h>
#include <stdio.h>

#define TEST(expect, expr)  do{ \
    if((expect) != (expr)){  fprintf(stderr, "Error @%d %s != %s\n",__LINE__,  #expect, #expr); __builtin_trap() ;abort();} \
  }while(0)

void testBitBuffer(){
  const uint8_t  d[] = {0b10101100, 0b00011010, 0b11110000, 0b10101010, 0b11001100 };
  const uint16_t l = sizeof(d);
  
  BitBuffer bb = BitBuffer_create(d, l);
  uint8_t b;
  TEST(1, b = BitBuffer_getBit(&bb)); // 0  // 0
  TEST(0, b = BitBuffer_getBit(&bb)); // 1
  TEST(1, b = BitBuffer_getBit(&bb)); // 2
  TEST(0, b = BitBuffer_getBit(&bb)); // 3
  TEST(1, b = BitBuffer_getBit(&bb)); // 4
  TEST(1, b = BitBuffer_getBit(&bb)); // 5
  TEST(0, b = BitBuffer_getBit(&bb)); // 6
  TEST(0, b = BitBuffer_getBit(&bb)); // 7
  TEST(0, b = BitBuffer_getBit(&bb)); // 0  // 1
  TEST(0, b = BitBuffer_getBit(&bb)); // 1
  TEST(0, b = BitBuffer_getBit(&bb)); // 2

  TEST(0b1101,     b = BitBuffer_getNBit(&bb, 4)); // 3 4 5 6
  TEST(0b0111100,  b = BitBuffer_getNBit(&bb, 7)); // 7    0 1 2 3 4 5  // 2 
  TEST(0b00101010, b = BitBuffer_getNBit(&bb, 8)); // 6 7  0 1 2 3 4 5  // 3
  TEST(0b10110011, b = BitBuffer_get8Bit(&bb));    // 6 7  0 1 2 3 4 5  // 4

  uint32_t c = 0;
  while(!BitBuffer_end(&bb)){
    ++c;
    b = BitBuffer_getBit(&bb);
  }
  TEST(2, c);
  
  bb = BitBuffer_create(d, l);
  for(int i=0; i<l; ++i){
    uint8_t h = BitBuffer_getNBit(&bb, 4);
    uint8_t l = BitBuffer_getNBit(&bb, 4);
    uint16_t v = (h << 4) | l;
    TEST(d[i], v);
  }
  bb = BitBuffer_create(d, l);
  for(int i=0; i<l; ++i){
    uint8_t v = BitBuffer_getNBit(&bb, 8);
    TEST(d[i], v);
  }
  bb = BitBuffer_create(d, l);
  for(int i=0; i<l; ++i){
    uint8_t v = BitBuffer_get8Bit(&bb);
    TEST(d[i], v);
  }

}

void putCharToOutput(char o){
  putchar(o);
}

int main()
{
  testBitBuffer();
  const CompressionData* cd = &CompD;
  char buf[20000];

  uint16_t oLen = uncompressToBuffer(cd, buf, 20000, compressed, sizeof(compressed));

  printf("uncompressed length: %d\n", oLen);
  printf(buf);

  uncompressToCB(cd, &putCharToOutput, compressed, sizeof(compressed));

}