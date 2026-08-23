/* Minimal, self-contained subset of the WDK's kbd.h.
 *
 * A Windows keyboard-layout DLL is nothing but a data blob: it exports
 * KbdLayerDescriptor(), which hands the kernel a KBDTABLES.  The real header
 * ships with the Driver Kit, which we do not want as a build dependency, so
 * the handful of structures we actually need are reproduced here.  Field
 * order and sizes are ABI -- do not reorder.
 *
 * Struct layout follows Microsoft's kbd.h; cross-checked against the
 * generated sources in lelegard/winkbdlayouts (BSD-2-Clause).
 *
 * Deliberately does not include <windows.h>, so this also compiles with a
 * host gcc for a syntax/shape check without a Windows toolchain.
 */
#ifndef UACC_KBD_H
#define UACC_KBD_H

#include <stddef.h>   /* wchar_t */

typedef unsigned char  BYTE;
typedef unsigned short WORD;
typedef unsigned short USHORT;
typedef wchar_t        WCHAR;   /* 16-bit under mingw; host check uses -fshort-wchar */
typedef unsigned int   DWORD;

#define MAKELONG(a, b) ((DWORD)(((WORD)(a)) | (((DWORD)((WORD)(b))) << 16)))

/* modifier bits */
#define KBDBASE        0x00
#define KBDSHIFT       0x01
#define KBDCTRL        0x02
#define KBDALT         0x04
#define SHFT_INVALID   0x0F

/* VK_TO_WCHARS attributes */
#define CAPLOK         0x01
#define SGCAPS         0x02
#define CAPLOKALTGR    0x04

/* wch sentinels */
#define WCH_NONE       0xF000
#define WCH_DEAD       0xF001
#define WCH_LGTR       0xF002

/* scancode-to-VK flags */
#define KBDEXT         (USHORT)0x0100
#define KBDMULTIVK     (USHORT)0x0200
#define KBDSPECIAL     (USHORT)0x0400
#define KBDNUMPAD      (USHORT)0x0800

#define VK__none_      0xFF

#define KLLF_ALTGR     0x0001
#define KBD_VERSION    1

typedef struct { BYTE Vk; BYTE ModBits; } VK_TO_BIT, *PVK_TO_BIT;

/* wMaxModBits == 7 means eight ModNumber slots.  The real header declares
 * ModNumber as a flexible array; gcc will not let us initialise one, and a
 * fixed eight-byte array is the identical binary layout. */
typedef struct { PVK_TO_BIT pVkToBit; WORD wMaxModBits; BYTE ModNumber[8]; }
    MODIFIERS, *PMODIFIERS;

typedef struct { BYTE VirtualKey; BYTE Attributes; WCHAR wch[1]; }
    VK_TO_WCHARS1, *PVK_TO_WCHARS1;
typedef struct { BYTE VirtualKey; BYTE Attributes; WCHAR wch[2]; }
    VK_TO_WCHARS2, *PVK_TO_WCHARS2;
typedef struct { BYTE VirtualKey; BYTE Attributes; WCHAR wch[3]; }
    VK_TO_WCHARS3, *PVK_TO_WCHARS3;
typedef struct { BYTE VirtualKey; BYTE Attributes; WCHAR wch[5]; }
    VK_TO_WCHARS5, *PVK_TO_WCHARS5;

typedef struct { PVK_TO_WCHARS1 pVkToWchars; BYTE nModifications; BYTE cbSize; }
    VK_TO_WCHAR_TABLE, *PVK_TO_WCHAR_TABLE;

typedef struct { DWORD dwBoth; WCHAR wchComposed; USHORT uFlags; }
    DEADKEY, *PDEADKEY;

typedef struct { BYTE vsc; WCHAR *pwsz; } VSC_LPWSTR, *PVSC_LPWSTR;
typedef struct { BYTE Vsc; USHORT Vk; } VSC_VK, *PVSC_VK;
typedef struct { BYTE VirtualKey; WORD ModificationNumber; WCHAR wch[1]; }
    LIGATURE1, *PLIGATURE1;

typedef struct tagKbdLayer {
    PMODIFIERS          pCharModifiers;
    PVK_TO_WCHAR_TABLE  pVkToWcharTable;
    PDEADKEY            pDeadKey;
    PVSC_LPWSTR         pKeyNames;
    PVSC_LPWSTR         pKeyNamesExt;
    WCHAR             **pKeyNamesDead;
    USHORT             *pusVSCtoVK;
    BYTE                bMaxVSCtoVK;
    PVSC_VK             pVSCtoVK_E0;
    PVSC_VK             pVSCtoVK_E1;
    DWORD               fLocaleFlags;
    BYTE                nLgMax;
    BYTE                cbLgEntry;
    PLIGATURE1          pLigature;
    DWORD               dwType;
    DWORD               dwSubType;
} KBDTABLES, *PKBDTABLES;

#define ARRAYSIZE(a) (sizeof(a) / sizeof((a)[0]))

/* The kernel walks these tables by raw size, so a wrong wchar_t width or a
 * stray padding byte silently corrupts every keystroke.  Catch it at compile
 * time instead. */
#define KBD_ASSERT_(c, n) typedef char kbd_assert_##n[(c) ? 1 : -1]
#define KBD_ASSERT__(c, n) KBD_ASSERT_(c, n)
#define KBD_ASSERT(c)      KBD_ASSERT__(c, __LINE__)
KBD_ASSERT(sizeof(WCHAR) == 2);
KBD_ASSERT(sizeof(VK_TO_WCHARS1) == 4);
KBD_ASSERT(sizeof(VK_TO_WCHARS2) == 6);
KBD_ASSERT(sizeof(VK_TO_WCHARS3) == 8);
KBD_ASSERT(sizeof(VK_TO_WCHARS5) == 12);
KBD_ASSERT(sizeof(VK_TO_BIT) == 2);
KBD_ASSERT(sizeof(VSC_VK) == 4);

#endif /* UACC_KBD_H */
