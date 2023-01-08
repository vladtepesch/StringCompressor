
#include "StringDecompressor.h"

#define STRINGDECOMPRESSOR_REST_SYM 255U

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



uint16_t decompressToCB(const CompressionData* i_cd, 
                              CharCallback     o_charOut, 
                              void*           io_callBackUserData,
                        const uint8_t*         i_compressed, 
                              uint16_t         i_cLen)
{
  uint16_t c = 0;
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
            if (nId == STRINGDECOMPRESSOR_REST_SYM){
//                print("    rest - reading addional bits ")
                sym = BitBuffer_get8Bit(&bb);
            }else{
                sym = nId;
            }
//            print("  symbol: ", ord(sym), " '", sym, "'")
            o_charOut(sym, io_callBackUserData);
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

uint16_t decompressToBuffer(const CompressionData* i_cd, char* o_buf, uint16_t i_maxOL, const uint8_t* i_compressed, uint16_t i_cLen )
{
  const char* bufStart = o_buf;
  BitBuffer bb = BitBuffer_create(i_compressed, i_cLen);
  
  // throw away padded 0 and start bit
  while(!BitBuffer_getBit(&bb));

  while((i_maxOL > 0) && !BitBuffer_end(&bb)){
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
            if (nId == STRINGDECOMPRESSOR_REST_SYM){
//                print("    rest - reading addional bits ")
                sym = BitBuffer_get8Bit(&bb);
            }else{
                sym = nId;
            }
//            print("  symbol: ", ord(sym), " '", sym, "'")
            *o_buf++ = sym;
            i_maxOL--;
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
