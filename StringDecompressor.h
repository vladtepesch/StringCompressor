
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>


#ifndef STRINGDECOMPRESSOR_H
#define STRINGDECOMPRESSOR_H

/// handle structure with pointer to the data
/// block containing compression tree for the decompression  
typedef struct CompressionData{
  const uint8_t (* data)[2];
}CompressionData;


/// function pointer for callback that outputs one decoded character
typedef void (*CharCallback)(char);

/**
 * decodes the compressed data to a output buffer
 * 
 * @param i_cd          Meta data for compression (symbol tree)
 * @param o_buf         output buffer to which the decoded data is written
 * @param i_maxOL       maximum number the output buffer can receive
 * @param i_compressed  compressed data bytes
 * @param i_cLen        length of compressed data bytes
 * @return  number of decoded bytes
 */
uint16_t uncompressToBuffer(const CompressionData* i_cd, 
                                  char*            o_buf, 
                                  uint16_t         i_maxOL, 
                            const uint8_t*         i_compressed, 
                                  uint16_t         i_cLen);

/**
 * decodes the compressed data and calls the o_charOut callback for each decoded byte
 * 
 * @param i_cd          Meta data for compression (symbol tree)
 * @param o_charOut     callbackk thats get called for each decoded byte
 * @param i_compressed  compressed data bytes
 * @param i_cLen        length of compressed data bytes
 * @return  number of decoded bytes
 */
uint16_t uncompressToCB(const CompressionData* i_cd, 
                              CharCallback     o_charOut, 
                        const uint8_t*         i_compressed, 
                              uint16_t         i_cLen);


/* some tool structures/function */

/** 
 * "class" that supports reading bitwise from a byte buffer.
 * Do not manually interfere with the structure members - use the related functions
 */
typedef struct BitBuffer{
  const uint8_t* data;
  uint16_t i;
  int8_t bi;
  uint16_t cache;
} BitBuffer;


/**
 * constructs a bitbuffer objects based on the given data and its length
 * 
 * @param data  pointer to data
 *              The pointer has to be valid as long the bitbuffer is used.
 * @param len   data length in bytes 
 * @returns initialized bitbuffer structure
 */
BitBuffer  BitBuffer_create(const uint8_t* data, uint16_t len);

/**
 * checks if the buffer is empty
 * 
 * @param bb[in,out]  bitbuffer instance
 * @returns true if buffer has no bits left
 */
bool BitBuffer_end(BitBuffer* bb);

/**
 * removes a single bit from the buffer
 * 
 * @param bb[in,out]  bitbuffer instance
 * @returns the removed bit
 */
uint8_t BitBuffer_getBit(BitBuffer* bb);

/**
 * removes up to 8 bit from the buffer
 * 
 * @param bb[in,out]  bitbuffer instance
 * @param n  n <= 8
 * @returns the removed bits
 */
uint8_t BitBuffer_getNBit(BitBuffer* bb, uint8_t n);

/**
 * removes 8 bit from the buffer
 * 
 * @param bb[in,out]  bitbuffer instance
 * @returns the removed bits
 */
uint8_t BitBuffer_get8Bit(BitBuffer* bb);

#endif // STRINGDECOMPRESSOR_H