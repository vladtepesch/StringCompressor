#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct CompressionData{
  const uint8_t (* data)[2];
}CompressionData;

typedef void (*CharCallback)(char);


#include "text.h"


typedef struct BitBuffer{
  const uint8_t* data;
  uint16_t i;
  int8_t bi;
  uint16_t cache;
} BitBuffer;

BitBuffer  BitBuffer_create(const uint8_t* data, uint16_t len){
  BitBuffer bb;
  bb.data = data+2;
  bb.i = len;
  bb.bi = 8;
  bb.cache = ((uint16_t)data[0])<<8 | data[1];
  return bb;
}

bool BitBuffer_end(BitBuffer* bb){
  return bb->i == 0;
}

uint8_t BitBuffer_loadFromBuffer(BitBuffer* bb){
  uint8_t r = 0;
  if( bb->i > 2){
    r = bb->data[0];
    bb->data++;
  }
  if(bb->i > 0){
    bb->i--;
  }
  return r;
}

uint8_t BitBuffer_getBit(BitBuffer* bb)
{
  uint8_t b = ((bb->cache) & 0x8000)?1:0;
  bb->cache = bb->cache << 1;
  bb->bi--;
  if (bb->bi == 0){
    bb->bi = 8;
    bb->cache = bb->cache | BitBuffer_loadFromBuffer(bb);
  } 
  return b;
}

/**
 * @param n  n <= 8
 */
uint8_t BitBuffer_getNBit(BitBuffer* bb, uint8_t n){
  uint8_t b = bb->cache >> (8+8-n);
  bb->cache = bb->cache << n;
  bb->bi -= n;
  if(bb->bi==0){
    bb->bi = 8;
    bb->cache = bb->cache | BitBuffer_loadFromBuffer(bb);
  }else if(bb->bi < 0){
    uint8_t d = -bb->bi;
    bb->bi = 8 - d;
    bb->cache = bb->cache | (BitBuffer_loadFromBuffer(bb) << d);
  }
  return b;
}


uint8_t BitBuffer_get8Bit(BitBuffer* bb){
  uint8_t b = bb->cache >> 8;
  bb->cache = bb->cache << 8;
  bb->cache = bb->cache | (((uint16_t)BitBuffer_loadFromBuffer(bb)) << (8-bb->bi));
  return b;
}


uint16_t uncompressToCB(const CompressionData* i_cd, CharCallback o_charOut, const uint8_t* i_compressed, uint16_t i_cLen )
{
  uint16_t c = 0;
  uint16_t Bi = 0;
  uint8_t  bi = 0;
  BitBuffer bb = BitBuffer_create(i_compressed, i_cLen);
  
  // throw away padded 0 and start bit
  while(!BitBuffer_getBit(&bb));

  while(!BitBuffer_end(&bb)){
    uint8_t s = 0;
    bool nextIsEnd[2] = {false, false};
    bool finishedSymbol = false;
    uint8_t sym;
    while (!finishedSymbol)
    {
        uint8_t bit = BitBuffer_getBit(&bb);
//        print("next bit: ", bit)
        uint8_t nId = i_cd->data[s][bit];
        if(nextIsEnd[bit])
        {
//            print("  is end: ")
            if (nId == 255){
//                print("    rest - reading addional bits ")
                sym = BitBuffer_get8Bit(&bb);
            }else{
                sym = nId;
            }
//            print("  symbol: ", ord(sym), " '", sym, "'")
            o_charOut(sym);
            c++;
            finishedSymbol = true;
        } else {
            nextIsEnd[0] = (nId & 0x80) != 0;
            nextIsEnd[1] = (nId & 0x40) != 0;
            s = nId & 0x3F;
//            print("  nextNodeId: ", s, " " ,nextIsEnd )
        }
    }
  }

  return c;
  //while(p < i_)
}

uint16_t uncompressToBuffer(const CompressionData* i_cd, char* o_buf, uint16_t i_maxOL, const uint8_t* i_compressed, uint16_t i_cLen )
{
  const char* bufStart = o_buf;
  uint16_t Bi = 0;
  uint8_t  bi = 0;
  BitBuffer bb = BitBuffer_create(i_compressed, i_cLen);
  
  // throw away padded 0 and start bit
  while(!BitBuffer_getBit(&bb));

  while(!BitBuffer_end(&bb)){
    uint8_t s = 0;
    bool nextIsEnd[2] = {false, false};
    bool finishedSymbol = false;
    uint8_t sym;
    while (!finishedSymbol)
    {
        uint8_t bit = BitBuffer_getBit(&bb);
//        print("next bit: ", bit)
        uint8_t nId = i_cd->data[s][bit];
        if(nextIsEnd[bit])
        {
//            print("  is end: ")
            if (nId == 255){
//                print("    rest - reading addional bits ")
                sym = BitBuffer_get8Bit(&bb);
            }else{
                sym = nId;
            }
//            print("  symbol: ", ord(sym), " '", sym, "'")
            *o_buf++ = sym;
            finishedSymbol = true;
        } else {
            nextIsEnd[0] = (nId & 0x80) != 0;
            nextIsEnd[1] = (nId & 0x40) != 0;
            s = nId & 0x3F;
//            print("  nextNodeId: ", s, " " ,nextIsEnd )
        }
    }
  }

  *o_buf = 0;
  return (uint16_t)(o_buf - bufStart);
  //while(p < i_)
}
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
  uint8_t buf[20000];

  uint16_t oLen = uncompressToBuffer(cd, buf, 20000, compressed, sizeof(compressed));

  printf("uncompressed length: %d\n", oLen);
  printf(buf);

  uncompressToCB(cd, &putCharToOutput, compressed, sizeof(compressed));

}