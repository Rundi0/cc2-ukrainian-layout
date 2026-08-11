#!/usr/bin/env python3
"""Install ua_cc system-wide and register it so desktops list it.

    sudo python3 linux/install.py            # install
    sudo python3 linux/install.py --remove   # undo

A copy in ~/.config/xkb is enough for libxkbcommon to *find* the layout, but
GNOME and KDE build their pickers from /usr/share/X11/xkb/rules, so anything
user-local never shows up in the UI.  Hence system-wide.
"""
import os
import shutil
import sys
import xml.etree.ElementTree as ET

XKB = '/usr/share/X11/xkb'
NAME = 'ua_cc'
DESC = 'Ukrainian (CharaChorder Two)'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', NAME)


def backup(path):
    if not os.path.exists(path + '.orig'):
        shutil.copy2(path, path + '.orig')


def edit_xml(remove):
    path = os.path.join(XKB, 'rules', 'evdev.xml')
    backup(path)
    # ElementTree drops the DOCTYPE, and the registry parsers want it back
    with open(path) as f:
        doctype = [l for l in f if l.startswith('<!DOCTYPE')]
    tree = ET.parse(path)
    layouts = tree.getroot().find('layoutList')
    for el in layouts.findall('layout'):
        if el.findtext('configItem/name') == NAME:
            layouts.remove(el)
    if not remove:
        el = ET.SubElement(layouts, 'layout')
        ci = ET.SubElement(el, 'configItem')
        ET.SubElement(ci, 'name').text = NAME
        ET.SubElement(ci, 'shortDescription').text = 'ua'
        ET.SubElement(ci, 'description').text = DESC
        ll = ET.SubElement(ci, 'languageList')
        ET.SubElement(ll, 'iso639Id').text = 'ukr'
        ET.SubElement(el, 'variantList')
    tree.write(path, encoding='UTF-8', xml_declaration=True)
    if doctype:
        with open(path) as f:
            head, _, rest = f.read().partition('\n')
        with open(path, 'w') as f:
            f.write(head + '\n' + doctype[0] + rest)


def edit_lst(remove):
    path = os.path.join(XKB, 'rules', 'evdev.lst')
    backup(path)
    with open(path) as f:
        lines = [l for l in f if not l.startswith('  %s ' % NAME)]
    if not remove:
        i = lines.index('! layout\n') + 1
        lines.insert(i, '  %-15s %s\n' % (NAME, DESC))
    with open(path, 'w') as f:
        f.writelines(lines)


def main():
    remove = '--remove' in sys.argv
    if os.geteuid() != 0:
        sys.exit('needs root: sudo python3 %s' % ' '.join(sys.argv))
    if not os.path.isdir(XKB):
        sys.exit('no %s -- install xkeyboard-config first' % XKB)

    dst = os.path.join(XKB, 'symbols', NAME)
    if remove:
        if os.path.exists(dst):
            os.remove(dst)
    else:
        shutil.copy(SRC, dst)
    edit_xml(remove)
    edit_lst(remove)

    print('removed' if remove else 'installed %s' % dst)
    if not remove:
        print('\nPick "%s" in your desktop\'s keyboard settings, or on X11:' % DESC)
        print('    setxkbmap %s' % NAME)
        print('\nA distro upgrade of xkeyboard-config rewrites rules/evdev.*;')
        print('re-run this script if the layout disappears from the list.')


if __name__ == '__main__':
    main()
