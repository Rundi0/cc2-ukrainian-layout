# Українська розкладка для CharaChorder Two

Реалізація специфікації з [`docs/layout-spec.md`](docs/layout-spec.md).

Одне джерело правди — таблиця `LAYOUT` у `gen.py`. Все інше генерується:

```
python3 gen.py
```

| файл | ОС |
|---|---|
| `out/ua_cc` | Linux (xkb symbols) |
| `out/ua_cc.klc` | Windows (MSKLC / kbdutool) |
| `out/ua_cc.keylayout` | macOS |
| `out/ua_cc.kcm` + `android/` | Android (APK з keyboard layout) |

`gen.py` при запуску сам перевіряє, що всі 33 літери, всі великі й уся ASCII-пунктуація десь досяжні.

## Розкладка

**Шар A1 (літери).** `q→я w→ш e→е r→р t→т y→и u→у i→і o→о p→п a→а s→с d→д f→ф g→г h→х j→й k→к l→л z→з x→ч c→ц v→в b→б n→н m→м`, плюс `;→ж '→ь ,→є .→ї -→щ /→'` і `IntlBackslash→ю` (ліва `index out`, тільки в профілі B).

**Шар A2 (пунктуація).**

| фізична клавіша | слот CC2 | base | Shift | AltGr | AltGr+Shift |
|---|---|---|---|---|---|
| `BracketLeft` | thumbMid out, **обидві руки** | `,` | `;` | `[` | `{` |
| `BracketRight` | thumbMid south, **обидві руки** | `.` | `:` | `]` | `}` |
| `Equal` | L ring out / R ring in | `-` | `=` | `+` | `_` |
| `Backquote` | L ring in | **ґ** | **Ґ** | `` ` `` | `~` |
| `Backslash` | L thumbEnd in | `\` | `\|` | | |
| `Digit0..9` | thumbTip/index/middle | `0..9` | `!@#$%^&*()` | | |

`?` лишається на Shift+`Slash` — права `thumbEnd north`, прямо з A1, без переходу на A2.

**Рівень AltGr** (права `little north`, десктоп): повертає все ASCII, що витіснила кирилиця, плюс українську типографіку.

| клавіша | AltGr | AltGr+Shift |
|---|---|---|
| `Quote` (ь) | `"` | `’` |
| `Comma` (є) | `<` | `«` |
| `Period` (ї) | `>` | `»` |
| `Semicolon` (ж) | `;` | `:` |
| `Minus` (щ) | `–` | `—` |
| `Slash` (') | `/` | |
| `KeyE` (е) | `€` | |
| `KeyG` (г) | `₴` | |

## Встановлення

### Linux

```bash
mkdir -p ~/.config/xkb/symbols
cp out/ua_cc ~/.config/xkb/symbols/
setxkbmap ua_cc          # X11, перевірити
```

Постійно — додати `ua_cc` у список розкладок GNOME/KDE через `~/.config/xkb/rules/evdev.xml`
(потрібно libxkbcommon ≥ 1.0; Wayland підхоплює `~/.config/xkb` без рута).
Системний варіант: `sudo cp out/ua_cc /usr/share/X11/xkb/symbols/`.

> Файл згенеровано, але **не скомпільовано** — `xkbcli` у цій системі немає.
> Перевір `xkbcli compile-keymap --layout ua_cc` перед тим, як покладатися.

### Windows

1. Відкрити `out/ua_cc.klc` у [MSKLC](https://www.microsoft.com/en-us/download/details.aspx?id=102134) → `Project → Build DLL and Setup Package`.
2. Або напряму: `kbdutool.exe -u -s ua_cc.klc`, потім інсталювати DLL.
3. Права адміністратора потрібні один раз, при встановленні.

VK-коди в `.klc` лишені **американські** (`Q` на скенкоді `10` і т.д.) — саме тому `Ctrl+C`/`Ctrl+V` працюють як завжди.

### macOS

```bash
cp out/ua_cc.keylayout ~/Library/Keyboard\ Layouts/
```

Перелогінитись, далі `System Settings → Keyboard → Input Sources → + → Others`.
Без підпису macOS 13+ може попросити підтвердження.

### Android

Готовий APK збирає CI на кожен пуш:
**[Releases → latest](https://github.com/Rundi0/cc2-ukrainian-layout/releases/tag/latest)**.
Локально — `cd android && gradle assembleDebug`.

1. Встановити APK (потрібен дозвіл на встановлення з невідомих джерел).
2. **Відкрити застосунок один раз.** Поки пакет не запускали, він у stopped-стані і система пропускає його, шукаючи розкладки.
3. Підключити CC2.
4. `Налаштування → Система → Клавіатура → Фізична клавіатура → CharaChorder Two → Ukrainian (CharaChorder Two)`.

Root не потрібен, `minSdk 21`. Розкладка видима лише поки пристрій підключений.

`android/debug.keystore` навмисно лежить у репозиторії: без фіксованого ключа кожна збірка CI підписувалась би новим, і оновлення падало б з `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. Це debug-ключ, довіряти йому нічого не варто.

## Відомі обмеження

- **Android: `\` і `|` недосяжні** в українському профілі. `generic.kl` мапить і `KEY_BACKSLASH` (43), і `KEY_102ND` (86) на той самий `KEYCODE_BACKSLASH`, а ми віддали цей keycode під **ю**. Перекрити `.kl` без рута не можна.
- **AltGr на Android** (`ralt:`) залежить від пристрою — Android часто ковтає правий Alt як меню-модифікатор. Все, що потрібно для звичайного тексту (`, . ; : - ? ! '`), доступне з base/Shift, без AltGr.
- **Linux, TUI-програми.** vim, tmux, i3, readline читають keysym активної групи, тому в українському режимі їхні гарячі клавіші зʼїдуть. GTK/Qt/Chromium мають latin-fallback і працюють. Обхід — перемикати профіль CC2, а не розкладку ОС.
- **xkb не скомпільовано** (див. вище).
- **`.klc` не зібрано** — MSKLC є тільки під Windows.
