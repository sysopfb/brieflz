/*
 * fast assembler crc32, header file
 *
 * Copyright (c) 1998-2003 by Joergen Ibsen / Jibz
 * All Rights Reserved
 *
 * http://www.ibsensoftware.com/
 */

#ifndef __CRC32_H_INCLUDED
#define __CRC32_H_INCLUDED

/* calling convention */
#ifndef BLZCC
 #ifdef __WATCOMC__
  #define BLZCC __cdecl
 #else
  #define BLZCC
 #endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* function prototypes */

unsigned int BLZCC is_crc32_asm_fast(const void *source,
                                     unsigned int length);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* __CRC32_H_INCLUDED */