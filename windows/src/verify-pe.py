#!/usr/bin/env python3
"""Check a built layout DLL against what win32k requires.

A keyboard layout DLL is loaded by the kernel, not by the normal user-mode
loader.  That imposes rules a plain `-shared` build does not meet, and getting
any of them wrong fails the same silent way: the layout still shows up in
Language options (that list is built from the registry) but never appears as a
usable input method.  Values here are what MSKLC produces.
"""
import struct
import sys

WANT = {'amd64': (0x8664, 0x180000000), 'i386': (0x014C, 0x10000000)}


def check(path, arch):
    b = open(path, 'rb').read()
    off = struct.unpack_from('<I', b, 0x3C)[0]
    if b[off:off + 4] != b'PE\0\0':
        return ['not a PE file']
    opt = off + 24
    p64 = struct.unpack_from('<H', b, opt)[0] == 0x20B
    machine = struct.unpack_from('<H', b, off + 4)[0]
    base = struct.unpack_from('<Q', b, opt + 24)[0] if p64 else \
        struct.unpack_from('<I', b, opt + 28)[0]
    subsystem = struct.unpack_from('<H', b, opt + 68)[0]
    dllchars = struct.unpack_from('<H', b, opt + 70)[0]
    dd = opt + (112 if p64 else 96)
    exp_rva, _ = struct.unpack_from('<II', b, dd)
    imp_rva, _ = struct.unpack_from('<II', b, dd + 8)
    nsec = struct.unpack_from('<H', b, off + 6)[0]
    sec = off + 24 + struct.unpack_from('<H', b, off + 20)[0]

    def to_off(rva):
        for i in range(nsec):
            vs, va, rs, ro = struct.unpack_from('<IIII', b, sec + i * 40 + 8)
            if va <= rva < va + max(vs, rs):
                return ro + (rva - va)
        return None

    imported = []
    if imp_rva:
        o = to_off(imp_rva)
        while o and b[o:o + 20] != b'\0' * 20:
            nrva = struct.unpack_from('<I', b, o + 12)[0]
            if not nrva:
                break
            no = to_off(nrva)
            imported.append(b[no:b.index(b'\0', no)].decode('latin1'))
            o += 20

    want_machine, want_base = WANT[arch]
    bad = []
    if machine != want_machine:
        bad.append('machine %#x, want %#x' % (machine, want_machine))
    if subsystem != 1:
        bad.append('subsystem %d, want 1 (NATIVE) -- the layout will be listed '
                   'but never selectable' % subsystem)
    if base != want_base:
        bad.append('image base %#x, want %#x' % (base, want_base))
    # ASLR/NX relocation of a kernel-loaded data blob is not wanted
    if dllchars & 0x0040:
        bad.append('DYNAMICBASE set')
    if dllchars & 0x0100:
        bad.append('NXCOMPAT set')
    if dllchars & 0x0020:
        bad.append('HIGH_ENTROPY_VA set')
    if not exp_rva:
        bad.append('no export directory')
    elif b'KbdLayerDescriptor' not in b:
        bad.append('KbdLayerDescriptor not exported')
    if imported:
        bad.append('imports %s; a layout DLL must import nothing'
                   % ', '.join(imported))
    return bad


if __name__ == '__main__':
    rc = 0
    for arg in sys.argv[1:]:
        arch = 'amd64' if 'amd64' in arg else 'i386'
        problems = check(arg, arch)
        if problems:
            rc = 1
            for p in problems:
                print('::error::%s: %s' % (arg, p))
        else:
            print('ok  %s (%s)' % (arg, arch))
    sys.exit(rc)
