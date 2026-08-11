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
sudo python3 linux/install.py            # встановити
sudo python3 linux/install.py --remove   # прибрати
```

Кладе `ua_cc` у `/usr/share/X11/xkb/symbols/` і реєструє в `rules/evdev.xml` та
`rules/evdev.lst`, після чого «Ukrainian (CharaChorder Two)» зʼявляється у
списку розкладок GNOME/KDE. Додай її там — тільки так вибір переживає перезахід:

```bash
gsettings set org.gnome.desktop.input-sources sources "[('xkb','us'),('xkb','ua_cc')]"
```

На X11 для поточної сесії — `setxkbmap us,ua_cc -option grp:win_space_toggle`.

> `setxkbmap` **замінює всю конфігурацію**, а не доповнює її. `setxkbmap ua_cc`
> лишить тебе з єдиною групою: без латиниці й без клавіші перемикання.
> Рятує `setxkbmap us`.

Системно, а не в `~/.config/xkb`, бо GNOME і KDE будують свій список саме з
`rules/` — користувацька копія працює для `xkbcommon`, але в UI не видно.
Оновлення пакета `xkeyboard-config` перезаписує `rules/evdev.*`; тоді просто
запусти скрипт ще раз. Оригінали зберігаються поруч як `evdev.xml.orig` і
`evdev.lst.orig`.

### Windows

PowerShell від адміністратора:

```powershell
.\windows\install.ps1
```

Копіює `uacc.dll` у `System32`/`SysWOW64`, реєструє KLID `a0000422`, і — головне —
прибирає `Layout Display Name`. Далі вийти з облікового запису і зайти назад,
потім `Параметри → Час і мова → Мова та регіон → Українська → Параметри мови →
Додати клавіатуру`. Видалення — `windows\uninstall.ps1`.

MSKLC потрібен **лише щоб зібрати** `uacc.dll` з `out/ua_cc.klc`
(`Project → Build DLL and Setup Package`), а не щоб її встановити. Готова DLL
лежить у `windows/`, тож на решті машин MSKLC не потрібен взагалі.

> **Чому окремий крок з `Layout Display Name`.** MSKLC 1.4 записує в реєстр
> посилання на строковий ресурс `@%SystemRoot%\system32\uacc.dll,-1000`, якого в
> зібраній DLL немає. Windows 11 не може розкрити назву і показує розкладку як
> «Unavailable input method»: вибрати мишкою ще можна, а `Win+Space` її пропускає.
> Прибирання цього значення повертає fallback на `Layout Text`.

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
- **`.keylayout` не перевірено на живій macOS** — файл валідний XML, але жодного разу не завантажувався в систему.

Перевірено: `out/ua_cc` компілюється `xkbcli compile-keymap` (libxkbcommon 1.4)
без помилок і дає очікувані символи; `.klc` зібрано MSKLC і встановлено; APK
збирає CI, `.kcm` усередині збігається з `gen.py` побайтово.
