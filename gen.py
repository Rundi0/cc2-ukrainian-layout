#!/usr/bin/env python3
"""Generate Ukrainian-for-CharaChorder-Two keyboard layouts for all four OSes.

Single source of truth is LAYOUT below: physical key -> (base, shift, altgr,
shift+altgr).  Everything else is a per-OS encoder.  Run `python3 gen.py` to
write out/.
"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'out'
NAME = 'Ukrainian (CharaChorder Two)'

# physical key -> (xkb name, PS/2 set-1 scancode, Windows VK, macOS vkey, Android kcm key)
KEYS = [
    ('Backquote',     'TLDE', 0x29, 'OEM_3',      50, 'GRAVE'),
    ('Digit1',        'AE01', 0x02, '1',          18, '1'),
    ('Digit2',        'AE02', 0x03, '2',          19, '2'),
    ('Digit3',        'AE03', 0x04, '3',          20, '3'),
    ('Digit4',        'AE04', 0x05, '4',          21, '4'),
    ('Digit5',        'AE05', 0x06, '5',          23, '5'),
    ('Digit6',        'AE06', 0x07, '6',          22, '6'),
    ('Digit7',        'AE07', 0x08, '7',          26, '7'),
    ('Digit8',        'AE08', 0x09, '8',          28, '8'),
    ('Digit9',        'AE09', 0x0a, '9',          25, '9'),
    ('Digit0',        'AE10', 0x0b, '0',          29, '0'),
    ('Minus',         'AE11', 0x0c, 'OEM_MINUS',  27, 'MINUS'),
    ('Equal',         'AE12', 0x0d, 'OEM_PLUS',   24, 'EQUALS'),
    ('KeyQ',          'AD01', 0x10, 'Q',          12, 'Q'),
    ('KeyW',          'AD02', 0x11, 'W',          13, 'W'),
    ('KeyE',          'AD03', 0x12, 'E',          14, 'E'),
    ('KeyR',          'AD04', 0x13, 'R',          15, 'R'),
    ('KeyT',          'AD05', 0x14, 'T',          17, 'T'),
    ('KeyY',          'AD06', 0x15, 'Y',          16, 'Y'),
    ('KeyU',          'AD07', 0x16, 'U',          32, 'U'),
    ('KeyI',          'AD08', 0x17, 'I',          34, 'I'),
    ('KeyO',          'AD09', 0x18, 'O',          31, 'O'),
    ('KeyP',          'AD10', 0x19, 'P',          35, 'P'),
    ('BracketLeft',   'AD11', 0x1a, 'OEM_4',      33, 'LEFT_BRACKET'),
    ('BracketRight',  'AD12', 0x1b, 'OEM_6',      30, 'RIGHT_BRACKET'),
    ('Backslash',     'BKSL', 0x2b, 'OEM_5',      42, 'BACKSLASH'),
    ('KeyA',          'AC01', 0x1e, 'A',           0, 'A'),
    ('KeyS',          'AC02', 0x1f, 'S',           1, 'S'),
    ('KeyD',          'AC03', 0x20, 'D',           2, 'D'),
    ('KeyF',          'AC04', 0x21, 'F',           3, 'F'),
    ('KeyG',          'AC05', 0x22, 'G',           5, 'G'),
    ('KeyH',          'AC06', 0x23, 'H',           4, 'H'),
    ('KeyJ',          'AC07', 0x24, 'J',          38, 'J'),
    ('KeyK',          'AC08', 0x25, 'K',          40, 'K'),
    ('KeyL',          'AC09', 0x26, 'L',          37, 'L'),
    ('Semicolon',     'AC10', 0x27, 'OEM_1',      41, 'SEMICOLON'),
    ('Quote',         'AC11', 0x28, 'OEM_7',      39, 'APOSTROPHE'),
    ('KeyZ',          'AB01', 0x2c, 'Z',           6, 'Z'),
    ('KeyX',          'AB02', 0x2d, 'X',           7, 'X'),
    ('KeyC',          'AB03', 0x2e, 'C',           8, 'C'),
    ('KeyV',          'AB04', 0x2f, 'V',           9, 'V'),
    ('KeyB',          'AB05', 0x30, 'B',          11, 'B'),
    ('KeyN',          'AB06', 0x31, 'N',          45, 'N'),
    ('KeyM',          'AB07', 0x32, 'M',          46, 'M'),
    ('Comma',         'AB08', 0x33, 'OEM_COMMA',  43, 'COMMA'),
    ('Period',        'AB09', 0x34, 'OEM_PERIOD', 47, 'PERIOD'),
    ('Slash',         'AB10', 0x35, 'OEM_2',      44, 'SLASH'),
    # ISO key.  Android's generic.kl maps BOTH 0x2b and 0x56 to BACKSLASH,
    # so on Android the two are indistinguishable -> Backslash (ю) wins and
    # this one is skipped there.  Elsewhere it keeps its US value.
    ('IntlBackslash', 'LSGT', 0x56, 'OEM_102',    10, 'BACKSLASH'),
]

# base, shift, altgr, shift+altgr.  '' = nothing on that level.
#
# Design rule: the US symbol plane is left COMPLETELY untouched -- every
# base/shift position keeps its American value.  The 26 Latin letter keys
# carry 26 Cyrillic letters, and the remaining 7 sit on AltGr of a letter
# key.  On the CC2 those 7 get a prepared combination each, so they stay a
# single press on layer A1.
LAYOUT = {
    # --- 26 letters on the 26 letter keys ---------------------------------
    'KeyO': 'оО', 'KeyA': 'аА', 'KeyN': 'нН', 'KeyY': 'иИ', 'KeyI': 'іІ',
    'KeyR': 'рР', 'KeyE': 'еЕ€', 'KeyU': 'уУ', 'KeyL': 'лЛ', 'KeyD': 'дД',
    'KeyP': 'пП', 'KeyM': 'мМ', 'KeyQ': 'яЯ', 'KeyG': 'гГ₴', 'KeyJ': 'йЙ',
    'KeyX': 'чЧ', 'KeyH': 'хХ', 'KeyW': 'шШ', 'KeyF': 'фФ',
    # --- 7 remaining letters on AltGr of a letter key ----------------------
    'KeyC': 'цЦїЇ',
    'KeyB': 'бБюЮ',
    'KeyZ': 'зЗщЩ',
    'KeyS': 'сСєЄ',
    'KeyV': 'вВжЖ',
    'KeyT': 'тТьЬ',
    'KeyK': 'кКґҐ',
    # --- punctuation: US base+shift, Ukrainian typography on AltGr ---------
    'Minus':  '-_–—',      # en dash / em dash
    'Comma':  ',<«',
    'Period': '.>»',
    'Quote':  '\'"’',
    # every other key is pure US -- see US below
}

US = {  # untouched keys, and the base/shift of anything LAYOUT leaves alone
    'Backquote': '`~', 'Digit1': '1!', 'Digit2': '2@', 'Digit3': '3#',
    'Digit4': '4$', 'Digit5': '5%', 'Digit6': '6^', 'Digit7': '7&',
    'Digit8': '8*', 'Digit9': '9(', 'Digit0': '0)', 'Minus': '-_',
    'Equal': '=+', 'BracketLeft': '[{', 'BracketRight': ']}',
    'Backslash': '\\|', 'Semicolon': ';:', 'Quote': '\'"', 'Comma': ',<',
    'Period': '.>', 'Slash': '/?', 'IntlBackslash': '\\|',
}
for _k in KEYS:
    if len(_k[0]) == 4 and _k[0].startswith('Key'):
        US[_k[0]] = _k[0][3].lower() + _k[0][3]


def levels(key):
    """-> [base, shift, altgr, shift+altgr], '' where unassigned."""
    s = LAYOUT.get(key) or US.get(key, '')
    return list(s) + [''] * (4 - len(s))


def is_alpha(key):
    b, s = levels(key)[:2]
    return b.isalpha() and s.isalpha() and b != s


def is_alpha4(key):
    """True when all four levels are letters -- CapsLock must reach AltGr too."""
    a, sa = levels(key)[2:]
    return is_alpha(key) and a.isalpha() and sa.isalpha() and a != sa


# ---------------------------------------------------------------- Linux ---
def xkb():
    L = ['// %s -- generated by gen.py, do not edit' % NAME,
         'default partial alphanumeric_keys modifier_keys',
         'xkb_symbols "basic" {', '', '    name[Group1] = "%s";' % NAME, '']
    for key, xk, *_ in KEYS:
        lv = levels(key)
        syms = ', '.join('U%04X' % ord(c) if c else 'NoSymbol' for c in lv)
        t = ('FOUR_LEVEL_ALPHABETIC' if is_alpha4(key) else
             'FOUR_LEVEL_SEMIALPHABETIC' if is_alpha(key) else 'FOUR_LEVEL')
        L.append('    key <%s> { type[Group1] = "%s", [ %s ] }; // %s'
                 % (xk, t, syms, key))
    L += ['', '    include "level3(ralt_switch)"', '};', '']
    return '\n'.join(L)


# -------------------------------------------------------------- Windows ---
KLC_HEAD = """KBD\tuacc\t"{name}"

COPYRIGHT\t"(c) 2026"
COMPANY\t"-"
LOCALENAME\t"uk-UA"
LOCALEID\t"00000422"
VERSION\t1.0
SHIFTSTATE

0\t//Column 4 : base
1\t//Column 5 : Shift
6\t//Column 6 : Ctrl+Alt (AltGr)
7\t//Column 7 : Shift+Ctrl+Alt

LAYOUT\t\t;an extra '@' at the end is a dead key

//SC\tVK_\t\tCap\t0\t1\t6\t7
//--\t----\t\t----\t----\t----\t----\t----
"""

KLC_TAIL = """
KEYNAME

01\tEsc
0e\tBackspace
0f\tTab
1c\tEnter
1d\tCtrl
2a\tShift
36\t"Right Shift"
37\t"Num *"
38\tAlt
39\tSpace
3a\t"Caps Lock"
3b\tF1
3c\tF2
3d\tF3
3e\tF4
3f\tF5
40\tF6
41\tF7
42\tF8
43\tF9
44\tF10
45\tPause
46\t"Scroll Lock"
47\t"Num 7"
48\t"Num 8"
49\t"Num 9"
4a\t"Num -"
4b\t"Num 4"
4c\t"Num 5"
4d\t"Num 6"
4e\t"Num +"
4f\t"Num 1"
50\t"Num 2"
51\t"Num 3"
52\t"Num 0"
53\t"Num Del"
54\t"Sys Req"
57\tF11
58\tF12

KEYNAME_EXT

1c\t"Num Enter"
1d\t"Right Ctrl"
35\t"Num /"
37\t"Prnt Scrn"
38\t"Right Alt"
45\t"Num Lock"
46\tBreak
47\tHome
48\tUp
49\t"Page Up"
4b\tLeft
4d\tRight
4f\tEnd
50\tDown
51\t"Page Down"
52\tInsert
53\tDelete
5b\t"Left Windows"
5c\t"Right Windows"
5d\tApplication

DESCRIPTIONS

0422\t{name}

LANGUAGENAMES

0422\tUkrainian (Ukraine)

ENDKBD
"""


def klc():
    L = [KLC_HEAD.format(name=NAME)]
    for key, _xk, sc, vk, *_ in KEYS:
        cols = '\t'.join('%04x' % ord(c) if c else '-1' for c in levels(key))
        L.append('%02x\t%s\t\t%d\t%s\t// %s'
                 % (sc, vk, 1 if is_alpha(key) else 0, cols, key))
    L.append('39\tSPACE\t\t0\t0020\t0020\t-1\t-1')
    L.append(KLC_TAIL.format(name=NAME))
    return '\n'.join(L).replace('\n', '\r\n')


# ---------------------------------------------------------------- macOS ---
def xesc(c):
    return {'&': '&#x0026;', '<': '&#x003C;', '>': '&#x003E;',
            '"': '&#x0022;', "'": '&#x0027;'}.get(c, c)


def keylayout():
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<!DOCTYPE keyboard SYSTEM '
         '"file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
         '<keyboard group="126" id="-31337" name="%s" maxout="1">' % NAME,
         '  <layouts>',
         '    <layout first="0" last="17" modifiers="mods" mapSet="set"/>',
         '  </layouts>',
         '  <modifierMap id="mods" defaultIndex="0">']
    # index 4 is the caps-lock map: letters uppercase, punctuation unchanged
    for i, mods in enumerate([['', 'caps anyShift'], ['anyShift'],
                              ['anyOption', 'caps anyOption'],
                              ['anyShift anyOption', 'caps anyShift anyOption'],
                              ['caps']]):
        L.append('    <keyMapSelect mapIndex="%d">' % i)
        L += ['      <modifier keys="%s"/>' % m for m in mods]
        L.append('    </keyMapSelect>')
    L += ['  </modifierMap>', '  <keyMapSet id="set">']
    for idx in range(5):
        L.append('    <keyMap index="%d">' % idx)
        for key, _xk, _sc, _vk, mac, _kcm in KEYS:
            c = levels(key)[1 if idx == 4 and is_alpha(key) else
                            0 if idx == 4 else idx]
            if c:
                L.append('      <key code="%d" output="%s"/>'
                         % (mac, xesc(c)))
        if idx in (0, 1):
            L.append('      <key code="49" output="&#x0020;"/>')
        L.append('    </keyMap>')
    L += ['  </keyMapSet>', '</keyboard>', '']
    return '\n'.join(L)


# -------------------------------------------------------------- Android ---
def kesc(c):
    if c == "'":
        return "'\\''"
    if c == '\\':
        return "'\\\\'"
    return "'%s'" % c if ord(c) < 128 else "'\\u%04x'" % ord(c)


def kcm():
    L = ['# %s -- generated by gen.py' % NAME, 'type OVERLAY', '']
    # Backslash and IntlBackslash collide on Android; Backslash carries ю,
    # so the ISO key is dropped and \ | are AltGr-only there.
    for key, _xk, _sc, _vk, _mac, kk in KEYS:
        if key not in LAYOUT or key == 'IntlBackslash':
            continue
        b, s, a, sa = levels(key)
        L.append('key %s {' % kk)
        L.append('    label:                              %s'
                 % kesc(s if is_alpha(key) else b))
        L.append('    base:                               %s' % kesc(b))
        if s and is_alpha(key):
            L.append('    shift, capslock:                    %s' % kesc(s))
            L.append('    shift+capslock:                     %s' % kesc(b))
        elif s:
            L.append('    shift:                              %s' % kesc(s))
        if a:
            L.append('    ralt:                               %s' % kesc(a))
        if sa:
            L.append('    shift+ralt:                         %s' % kesc(sa))
        L.append('}')
        L.append('')
    return '\n'.join(L)



# --------------------------------------------------- Windows: kbd DLL source ---
# MSKLC is a GUI tool that only runs on Windows, so CI cannot use it.  A layout
# DLL is just a data blob exporting KbdLayerDescriptor(), so we emit the C
# ourselves and cross-compile it with mingw-w64.  Column order in the wchar
# tables is fixed by char_modifiers below: base, shift, ctrl, altgr, altgr+shift.

def _vk(name):
    """gen.py VK spelling -> C token."""
    return "'%s'" % name if len(name) == 1 else 'VK_' + name


def _wch(c):
    if not c:
        return 'WCH_NONE'
    if c == "'":
        return "L'\\''"
    if c == '\\':
        return "L'\\\\'"
    return "L'%s'" % c if ord(c) < 128 else '0x%04X' % ord(c)


def _ctrl(vkname):
    """The control character US layouts put on Ctrl+key, or WCH_NONE."""
    if len(vkname) == 1 and vkname.isalpha():
        return '0x%04X' % (ord(vkname) - 0x40)
    return {'OEM_4': '0x001B', 'OEM_5': '0x001C', 'OEM_6': '0x001D'}.get(
        vkname, 'WCH_NONE')


# scancode -> VK for everything that is not a character key.  Character keys
# come from KEYS, so the American VK assignment stays the single source.
_VSC_FIXED = {
    0x00: 'VK__none_', 0x01: 'VK_ESCAPE', 0x0E: 'VK_BACK', 0x0F: 'VK_TAB',
    0x1C: 'VK_RETURN', 0x1D: 'VK_LCONTROL', 0x2A: 'VK_LSHIFT',
    0x36: 'VK_RSHIFT | KBDEXT', 0x37: 'VK_MULTIPLY | KBDMULTIVK',
    0x38: 'VK_LMENU', 0x39: 'VK_SPACE', 0x3A: 'VK_CAPITAL',
    0x45: 'VK_NUMLOCK | KBDEXT | KBDMULTIVK', 0x46: 'VK_SCROLL | KBDMULTIVK',
    0x4A: 'VK_SUBTRACT', 0x4E: 'VK_ADD', 0x54: 'VK_SNAPSHOT',
    0x55: 'VK__none_', 0x57: 'VK_F11', 0x58: 'VK_F12',
}
for _i in range(10):                        # F1..F10
    _VSC_FIXED[0x3B + _i] = 'VK_F%d' % (_i + 1)
for _sc, _v in [(0x47, 'HOME'), (0x48, 'UP'), (0x49, 'PRIOR'), (0x4B, 'LEFT'),
                (0x4C, 'CLEAR'), (0x4D, 'RIGHT'), (0x4F, 'END'),
                (0x50, 'DOWN'), (0x51, 'NEXT'), (0x52, 'INSERT'),
                (0x53, 'DELETE')]:
    _VSC_FIXED[_sc] = 'VK_%s | KBDSPECIAL | KBDNUMPAD' % _v

_KEY_NAMES = [
    (0x01, 'Esc'), (0x0E, 'Backspace'), (0x0F, 'Tab'), (0x1C, 'Enter'),
    (0x1D, 'Ctrl'), (0x2A, 'Shift'), (0x36, 'Right Shift'), (0x37, 'Num *'),
    (0x38, 'Alt'), (0x39, 'Space'), (0x3A, 'Caps Lock'), (0x45, 'Pause'),
    (0x46, 'Scroll Lock'), (0x47, 'Num 7'), (0x48, 'Num 8'), (0x49, 'Num 9'),
    (0x4A, 'Num -'), (0x4B, 'Num 4'), (0x4C, 'Num 5'), (0x4D, 'Num 6'),
    (0x4E, 'Num +'), (0x4F, 'Num 1'), (0x50, 'Num 2'), (0x51, 'Num 3'),
    (0x52, 'Num 0'), (0x53, 'Num Del'), (0x54, 'Sys Req'), (0x57, 'F11'),
    (0x58, 'F12'),
] + [(0x3B + i, 'F%d' % (i + 1)) for i in range(10)]

_KEY_NAMES_EXT = [
    (0x1C, 'Num Enter'), (0x1D, 'Right Ctrl'), (0x35, 'Num /'),
    (0x37, 'Prnt Scrn'), (0x38, 'Right Alt'), (0x45, 'Num Lock'),
    (0x46, 'Break'), (0x47, 'Home'), (0x48, 'Up'), (0x49, 'Page Up'),
    (0x4B, 'Left'), (0x4D, 'Right'), (0x4F, 'End'), (0x50, 'Down'),
    (0x51, 'Page Down'), (0x52, 'Insert'), (0x53, 'Delete'),
    (0x5B, 'Left Windows'), (0x5C, 'Right Windows'), (0x5D, 'Application'),
]

_E0 = [(0x1C, 'VK_RETURN'), (0x1D, 'VK_RCONTROL'), (0x35, 'VK_DIVIDE'),
       (0x37, 'VK_SNAPSHOT'), (0x38, 'VK_RMENU'), (0x47, 'VK_HOME'),
       (0x48, 'VK_UP'), (0x49, 'VK_PRIOR'), (0x4B, 'VK_LEFT'),
       (0x4D, 'VK_RIGHT'), (0x4F, 'VK_END'), (0x50, 'VK_DOWN'),
       (0x51, 'VK_NEXT'), (0x52, 'VK_INSERT'), (0x53, 'VK_DELETE'),
       (0x5B, 'VK_LWIN'), (0x5C, 'VK_RWIN'), (0x5D, 'VK_APPS')]


def kbd_c():
    L = ['/* %s -- generated by gen.py, do not edit.' % NAME,
         ' *',
         ' * Windows keyboard layout DLL source.  Built by',
         ' * .github/workflows/windows.yml with mingw-w64; no MSKLC, no WDK.',
         ' */',
         '#include "kbd.h"',
         '#include "vk.h"',
         '',
         'static VK_TO_BIT vk_to_bits[] = {',
         '    {VK_SHIFT,   KBDSHIFT},',
         '    {VK_CONTROL, KBDCTRL},',
         '    {VK_MENU,    KBDALT},',
         '    {0,          0}',
         '};',
         '',
         'static MODIFIERS char_modifiers = {',
         '    vk_to_bits, 7, {',
         '        0,            /* 000 base                  */',
         '        1,            /* 001 Shift                 */',
         '        2,            /* 010 Ctrl                  */',
         '        SHFT_INVALID, /* 011 Shift Ctrl            */',
         '        SHFT_INVALID, /* 100 Alt                   */',
         '        SHFT_INVALID, /* 101 Shift Alt             */',
         '        3,            /* 110 Ctrl Alt   = AltGr    */',
         '        4,            /* 111 Shift Ctrl Alt        */',
         '    }',
         '};',
         '',
         '/*                        base      shift     ctrl      altgr     altgr+shift */',
         'static VK_TO_WCHARS5 vk_to_wchar5[] = {']
    for key, _xk, _sc, vk, _mac, _kk in KEYS:
        b, s, a, sa = levels(key)
        attr = 'CAPLOK | CAPLOKALTGR' if is_alpha4(key) else \
               'CAPLOK' if is_alpha(key) else '0x00'
        L.append('    {%-13s %-21s {%-9s %-9s %-9s %-9s %-9s}}, /* %s */'
                 % (_vk(vk) + ',', attr + ',',
                    _wch(b) + ',', _wch(s) + ',', _ctrl(vk) + ',',
                    _wch(a) + ',', _wch(sa), key))
    L += ['    {0, 0, {0, 0, 0, 0, 0}}',
          '};',
          '',
          'static VK_TO_WCHARS3 vk_to_wchar3[] = {',
          "    {VK_BACK,   0x00, {0x0008, 0x0008, 0x007F}},",
          "    {VK_ESCAPE, 0x00, {0x001B, 0x001B, 0x001B}},",
          "    {VK_RETURN, 0x00, {L'\\r',  L'\\r',  L'\\n'}},",
          "    {VK_SPACE,  0x00, {L' ',   L' ',   L' '}},",
          "    {VK_CANCEL, 0x00, {0x0003, 0x0003, 0x0003}},",
          '    {0, 0, {0, 0, 0}}',
          '};',
          '',
          'static VK_TO_WCHARS2 vk_to_wchar2[] = {',
          "    {VK_TAB,      0x00, {L'\\t', L'\\t'}},",
          "    {VK_ADD,      0x00, {L'+',  L'+'}},",
          "    {VK_DIVIDE,   0x00, {L'/',  L'/'}},",
          "    {VK_MULTIPLY, 0x00, {L'*',  L'*'}},",
          "    {VK_SUBTRACT, 0x00, {L'-',  L'-'}},",
          '    {0, 0, {0, 0}}',
          '};',
          '',
          'static VK_TO_WCHARS1 vk_to_wchar1[] = {']
    for d in range(10):
        L.append("    {VK_NUMPAD%d, 0x00, {L'%d'}}," % (d, d))
    L += ["    {VK_DECIMAL, 0x00, {L'.'}},",
          '    {0, 0, {0}}',
          '};',
          '',
          'static VK_TO_WCHAR_TABLE vk_to_wchar[] = {',
          '    {(PVK_TO_WCHARS1)vk_to_wchar5, 5, sizeof(vk_to_wchar5[0])},',
          '    {(PVK_TO_WCHARS1)vk_to_wchar3, 3, sizeof(vk_to_wchar3[0])},',
          '    {(PVK_TO_WCHARS1)vk_to_wchar2, 2, sizeof(vk_to_wchar2[0])},',
          '    {(PVK_TO_WCHARS1)vk_to_wchar1, 1, sizeof(vk_to_wchar1[0])},',
          '    {NULL, 0, 0}',
          '};',
          '',
          'static DEADKEY dead_keys[] = { {0, 0, 0} };',
          'static WCHAR *key_names_dead[] = { NULL };',
          '',
          'static VSC_LPWSTR key_names[] = {']
    for sc, nm in sorted(_KEY_NAMES):
        L.append('    {0x%02X, L"%s"},' % (sc, nm))
    L += ['    {0x00, NULL}', '};', '', 'static VSC_LPWSTR key_names_ext[] = {']
    for sc, nm in sorted(_KEY_NAMES_EXT):
        L.append('    {0x%02X, L"%s"},' % (sc, nm))
    L += ['    {0x00, NULL}', '};', '', 'static USHORT scancode_to_vk[] = {']
    by_sc = {sc: vk for _k, _x, sc, vk, _m, _kk in KEYS}
    for sc in range(0x59):
        if sc in by_sc:
            tok = _vk(by_sc[sc])
        else:
            tok = _VSC_FIXED.get(sc, 'VK__none_')
        L.append('    /* %02X */ %s,' % (sc, tok))
    L += ['};', '', 'static VSC_VK scancode_to_vk_e0[] = {']
    for sc, vk in _E0:
        L.append('    {0x%02X, %s | KBDEXT},' % (sc, vk))
    L += ['    {0x00, 0x0000}', '};', '',
          'static VSC_VK scancode_to_vk_e1[] = {',
          '    {0x1D, VK_PAUSE},',
          '    {0x00, 0x0000}',
          '};',
          '',
          'static KBDTABLES kbd_tables = {',
          '    .pCharModifiers  = &char_modifiers,',
          '    .pVkToWcharTable = vk_to_wchar,',
          '    .pDeadKey        = dead_keys,',
          '    .pKeyNames       = key_names,',
          '    .pKeyNamesExt    = key_names_ext,',
          '    .pKeyNamesDead   = key_names_dead,',
          '    .pusVSCtoVK      = scancode_to_vk,',
          '    .bMaxVSCtoVK     = ARRAYSIZE(scancode_to_vk),',
          '    .pVSCtoVK_E0     = scancode_to_vk_e0,',
          '    .pVSCtoVK_E1     = scancode_to_vk_e1,',
          '    .fLocaleFlags    = MAKELONG(KLLF_ALTGR, KBD_VERSION),',
          '    .nLgMax          = 0,',
          '    .cbLgEntry       = 0,',
          '    .pLigature       = NULL,',
          '    .dwType          = 4,',
          '    .dwSubType       = 0,',
          '};',
          '',
          'KBD_EXPORT PKBDTABLES KbdLayerDescriptor(void)',
          '{',
          '    return &kbd_tables;',
          '}',
          '']
    return '\n'.join(L)



# ----------------------------------------------------- Windows: registry ---
# Shipped as generated output rather than an MSKLC export, because MSKLC's
# export names two string resources (-1000, -1100) that our DLL does not
# contain.  Windows cannot resolve them, and an input method whose display
# name will not resolve is listed under Language options but never offered as
# a keyboard.  We register only fields we actually back.
KLID = 'a0000422'
LAYOUT_ID = '00c0'


def reg():
    return '\r\n'.join([
        'Windows Registry Editor Version 5.00',
        '',
        r'[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard '
        r'Layouts\%s]' % KLID,
        '"Layout Text"="%s"' % NAME,
        '"Layout File"="uacc.dll"',
        '"Layout Id"="%s"' % LAYOUT_ID,
        '',
    ])


# ----------------------------------------------------------------- check ---
def check():
    ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    base = {}
    for key, *_ in KEYS:
        # the ISO key is a deliberate US duplicate of Backslash
        if key == 'IntlBackslash':
            continue
        for lvl, c in enumerate(levels(key)):
            if c:
                assert (lvl, c) not in base, 'duplicate %r on %s and %s' % (
                    c, base[(lvl, c)], key)
                base[(lvl, c)] = key
    missing = [c for c in ALPHABET
               if not any((lvl, c) in base for lvl in range(4))]
    assert not missing, 'missing letters: %s' % ''.join(missing)
    missing = [c.upper() for c in ALPHABET
               if not any((lvl, c.upper()) in base for lvl in range(4))]
    assert not missing, 'missing capitals: %s' % ''.join(missing)
    for c in "'.,;:?!-()\"[]{}<>/\\`~@#$%^&*_+=|":
        assert any((lvl, c) in base for lvl in range(4)), 'no way to type %r' % c
    # Android: BACKSLASH is claimed once, by ю
    kcm_keys = [k[5] for k in KEYS if k[0] in LAYOUT and k[0] != 'IntlBackslash']
    assert len(kcm_keys) == len(set(kcm_keys)), 'unexpected kcm collisions'
    print('check ok: 33 letters + capitals + all ASCII punctuation reachable')


if __name__ == '__main__':
    check()
    OUT.mkdir(exist_ok=True)
    for fn, txt in [('ua_cc', xkb()), ('ua_cc.klc', klc()),
                    ('ua_cc.keylayout', keylayout()), ('ua_cc.kcm', kcm())]:
        p = OUT / fn
        # MSKLC writes and expects .klc as UTF-16LE with a BOM
        p.write_bytes(txt.encode('utf-16-le' if fn.endswith('.klc')
                                 else 'utf-8'))
        if fn.endswith('.klc'):
            p.write_bytes(b'\xff\xfe' + p.read_bytes())
        print('%-22s %5d bytes' % (p.name, p.stat().st_size))
    winsrc = OUT.parent / 'windows/src/uacc.c'
    if winsrc.parent.is_dir():
        # write_bytes, not write_text: write_text translates \n to \r\n on
        # Windows, so the file CI hashes would not be the file git stores
        winsrc.write_bytes(kbd_c().encode('utf-8'))
        print('%-22s -> MSVC build' % winsrc.name)
    winreg = OUT.parent / 'windows/uacc.reg'
    if winreg.parent.is_dir():
        winreg.write_bytes(b'\xff\xfe' + reg().encode('utf-16-le'))
        print('%-22s -> registry' % winreg.name)
    raw = OUT.parent / 'android/app/src/main/res/raw/ua_cc.kcm'
    if raw.parent.is_dir():
        raw.write_bytes(kcm().encode('utf-8'))
        print('%-22s -> android APK' % raw.name)
