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
LAYOUT = {
    # --- CC2 layer A1: the 33 Cyrillic letters + apostrophe ---------------
    'KeyO': 'оО', 'KeyA': 'аА', 'KeyN': 'нН', 'KeyY': 'иИ', 'KeyI': 'іІ',
    'KeyV': 'вВ', 'KeyT': 'тТ', 'KeyR': 'рР', 'KeyE': 'еЕ€',  'KeyS': 'сС',
    'KeyK': 'кК', 'KeyU': 'уУ', 'KeyL': 'лЛ', 'KeyD': 'дД', 'KeyP': 'пП',
    'KeyM': 'мМ', 'KeyZ': 'зЗ', 'KeyQ': 'яЯ', 'KeyB': 'бБ', 'KeyG': 'гГ₴',
    'KeyJ': 'йЙ', 'KeyX': 'чЧ', 'KeyH': 'хХ', 'KeyC': 'цЦ', 'KeyW': 'шШ',
    'KeyF': 'фФ',
    'Quote':         'ьЬ"’',
    'Comma':         'єЄ<«',
    'Period':        'їЇ>»',
    'Semicolon':     'жЖ;:',
    'Minus':         'щЩ–—',      # en dash / em dash
    'Slash':         "'?/",       # ? stays where it always was: Shift+Slash
    # --- CC2 layer A2: punctuation + the one spilled letter ---------------
    'Backquote':    'ґҐ`~',
    'BracketLeft':  ',;[{',
    'BracketRight': '.:]}',
    'Equal':        '-=+_',
    'Backslash':    'юЮ\\|',   # CC2: right `index out`, was SpaceRight
    # digits keep their US values (see US below)
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


# ---------------------------------------------------------------- Linux ---
def xkb():
    L = ['// %s -- generated by gen.py, do not edit' % NAME,
         'default partial alphanumeric_keys modifier_keys',
         'xkb_symbols "basic" {', '', '    name[Group1] = "%s";' % NAME, '']
    for key, xk, *_ in KEYS:
        lv = levels(key)
        syms = ', '.join('U%04X' % ord(c) if c else 'NoSymbol' for c in lv)
        t = 'FOUR_LEVEL_SEMIALPHABETIC' if is_alpha(key) else 'FOUR_LEVEL'
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


# ----------------------------------------------------------------- check ---
def check():
    ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    base = {}
    for key, *_ in KEYS:
        for lvl, c in enumerate(levels(key)):
            if c:
                assert (lvl, c) not in base, 'duplicate %r on %s and %s' % (
                    c, base[(lvl, c)], key)
                base[(lvl, c)] = key
    missing = [c for c in ALPHABET if (0, c) not in base]
    assert not missing, 'missing letters: %s' % ''.join(missing)
    missing = [c.upper() for c in ALPHABET if (1, c.upper()) not in base]
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
    raw = OUT.parent / 'android/app/src/main/res/raw/ua_cc.kcm'
    if raw.parent.is_dir():
        raw.write_bytes(kcm().encode('utf-8'))
        print('%-22s -> android APK' % raw.name)
