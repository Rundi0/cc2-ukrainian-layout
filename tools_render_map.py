#!/usr/bin/env python3
"""Render the CC2 key map (3 layers x 2 hands x 9 switches x 5 directions)
as a self-contained HTML page."""
import importlib.util
import json
import pathlib

HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('gen', '/home/user/cc2-ukrainian/gen.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

SHORT = {
    'SpaceLeft': '␣', 'SpaceRight': '␣', 'Enter': '⏎', 'Tab': '⇥',
    'Escape': 'esc', 'Backspace': '⌫', 'CapsLock': 'caps',
    'ShiftLeft': '⇧', 'ShiftRight': '⇧', 'ControlLeft': 'ctrl',
    'ControlRight': 'ctrl', 'AltLeft': 'alt', 'AltRight': 'altgr',
    'MetaLeft': 'meta', 'MetaRight': 'meta',
    'SecondaryKeymapLeft': 'A2', 'SecondaryKeymapRight': 'A2',
    'TertiaryKeymapLeft': 'A3', 'TertiaryKeymapRight': 'A3',
    'AmbidextrousThrowoverLeft': 'ambi', 'AmbidextrousThrowoverRight': 'ambi',
    'Dup': 'dup', 'MouseLeftClick': 'ЛКМ', 'MouseRightClick': 'ПКМ',
    'MouseMoveUp': '↑', 'MouseMoveDown': '↓', 'MouseMoveLeft': '←',
    'MouseMoveRight': '→', 'MouseScrollCoastUp': '≡↑',
    'MouseScrollCoastDown': '≡↓', 'MouseScrollCoastLeft': '≡←',
    'MouseScrollCoastRight': '≡→',
    'ArrowUp': '↑', 'ArrowDown': '↓', 'ArrowLeft': '←', 'ArrowRight': '→',
}
CYR = set('абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ')
# the one slot the plan needs but the Device Manager will not expose
BLOCKED = {'IntlBackslash'}


def cell(slot):
    """-> dict the front end renders directly."""
    kind, key, label, sh = slot['kind'], slot['key'], slot['label'], slot['shift']
    out = {'k': kind, 'note': ''}
    if kind == 'chord':
        out.update(k='chord', ua='·', en='·', note='вхід акорду — не чіпати')
        return out
    if kind == 'free':
        out.update(ua='', en='')
        return out
    if kind in ('mod', 'special'):
        out.update(k='sys' if kind == 'special' else 'mod',
                   ua=SHORT.get(label, label), en=SHORT.get(label, label),
                   note=label)
        return out
    lay = gen.LAYOUT.get(key)
    us = gen.US.get(key)
    idx = 1 if sh else 0
    ua = (lay or us or ['?'])[idx] if (lay or us) else key
    en = (us or ['?'])[idx] if us else SHORT.get(key, key)
    if not us:                       # Space, Enter, arrows, F-keys...
        ua = en = SHORT.get(key, key)
        out.update(k='sys', ua=ua, en=en, note=key)
        return out
    out.update(k='ukr' if ua in CYR else 'sym', ua=ua, en=en, note=key)
    return out


def build():
    slots = json.load(open(HERE / 'slots.json'))
    data = {}
    for s in slots:
        data['%d%s%s%s' % (s['layer'], s['half'], s['sw'], s['dir'])] = cell(s)
    # the one slot the Ukrainian profile reassigns: SpaceRight -> Backslash
    data['1Rindexout'] = {'k': 'moved', 'ua': 'ю', 'en': '␣',
        'note': 'єдина правка в CC2: SpaceRight -> Backslash. '
                'Лівий пробіл лишається'}
    return data


TEMPLATE = r'''<title>Мапа клавіш CharaChorder Two</title>
<style>
:root{
  --ground:#EDF0F3; --surface:#FFFFFF; --sunk:#E3E8ED;
  --ink:#131A21; --muted:#5E6D7C; --line:#CBD4DC; --hair:#DDE4EA;
  --letter:#14539A; --letter-bg:#DCE8F6;
  --sym:#2C4A5E; --sym-bg:#E4EBF0;
  --free:#A96F00; --free-bg:#FBF0DA;
  --stop:#B03030;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0D1218; --surface:#151C24; --sunk:#101820;
    --ink:#E6ECF2; --muted:#8FA0B0; --line:#2A3641; --hair:#212B34;
    --letter:#6FAAEC; --letter-bg:#14263C;
    --sym:#9FBACD; --sym-bg:#1A242E;
    --free:#F0B429; --free-bg:#2E2410;
    --stop:#E87A6E;
  }
}
:root[data-theme="dark"]{
  --ground:#0D1218; --surface:#151C24; --sunk:#101820;
  --ink:#E6ECF2; --muted:#8FA0B0; --line:#2A3641; --hair:#212B34;
  --letter:#6FAAEC; --letter-bg:#14263C;
  --sym:#9FBACD; --sym-bg:#1A242E;
  --free:#F0B429; --free-bg:#2E2410;
  --stop:#E87A6E;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
.wrap{max-width:1180px;margin:0 auto;padding:40px 24px 80px}
.mono{font-family:ui-monospace,SFMono-Regular,"Cascadia Mono",Menlo,Consolas,monospace}
.eyebrow{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);
}
h1{font-size:clamp(26px,4vw,38px);line-height:1.15;margin:.3em 0 .2em;text-wrap:balance;
   letter-spacing:-.015em}
h2{font-size:22px;margin:0 0 .4em;letter-spacing:-.01em;text-wrap:balance}
p{max-width:66ch;color:var(--ink)}
.lede{color:var(--muted);max-width:64ch}
header{border-bottom:1px solid var(--line);padding-bottom:28px;margin-bottom:28px}

.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 22px}
.seg{display:flex;border:1px solid var(--line);border-radius:2px;overflow:hidden;background:var(--surface)}
.seg button{
  font-family:ui-monospace,Menlo,monospace;font-size:12px;letter-spacing:.1em;
  text-transform:uppercase;padding:9px 16px;border:0;background:transparent;
  color:var(--muted);cursor:pointer;border-right:1px solid var(--hair);
}
.seg button:last-child{border-right:0}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}
.seg button:focus-visible{outline:2px solid var(--letter);outline-offset:-2px}

.board{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
.hand{background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:18px 16px 16px;
      overflow-x:auto}
.hand > .eyebrow{margin-bottom:14px}
.row{display:flex;gap:12px;margin-bottom:12px;justify-content:center}
.row:last-child{margin-bottom:0}
.sw{width:104px;flex:0 0 auto}
.sw .nm{
  font-family:ui-monospace,Menlo,monospace;font-size:9.5px;letter-spacing:.07em;
  color:var(--muted);text-align:center;margin-bottom:4px;text-transform:uppercase;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.rose{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,26px);gap:2px}
.c{
  display:flex;align-items:center;justify-content:center;border-radius:2px;
  font-size:14px;line-height:1;background:var(--sunk);color:var(--muted);
  border:1px solid transparent;min-width:0;overflow:hidden;
}
.c.sm{font-size:9.5px;font-family:ui-monospace,Menlo,monospace;letter-spacing:.02em}
.c.ukr{background:var(--letter-bg);color:var(--letter);font-weight:650;font-size:16px;
       border-color:color-mix(in srgb,var(--letter) 22%,transparent)}
.c.sym{background:var(--sym-bg);color:var(--sym);font-weight:600}
.c.mod,.c.sys{background:transparent;border:1px dashed var(--hair);color:var(--muted)}
.c.chord{background:transparent;border:1px solid var(--hair);color:var(--hair)}
.c.free{background:transparent;border:1px dashed var(--free);color:var(--free)}
.c.moved{background:var(--free-bg);color:var(--free);border:1px solid var(--free);
         font-weight:650;font-size:16px}
.c.gap{background:transparent;border:0}

.legend{display:flex;flex-wrap:wrap;gap:8px 20px;margin:24px 0 0;padding-top:18px;
        border-top:1px solid var(--hair)}
.lg{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted)}
.sq{width:16px;height:16px;border-radius:2px;flex:0 0 auto}

section{margin-top:52px}
table{border-collapse:collapse;width:100%;font-size:14.5px;margin-top:12px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--hair);vertical-align:top}
th{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;letter-spacing:.12em;
   text-transform:uppercase;color:var(--muted);font-weight:500}
td.n{font-variant-numeric:tabular-nums;white-space:nowrap}
.scroll{overflow-x:auto}
.callout{border-left:3px solid var(--free);background:var(--free-bg);padding:14px 18px;
         border-radius:0 3px 3px 0;margin:20px 0}
.callout p{margin:0;max-width:62ch}
kbd{font-family:ui-monospace,Menlo,monospace;font-size:.86em;background:var(--sunk);
    border:1px solid var(--hair);border-radius:2px;padding:1px 5px}
@media (max-width:860px){.board{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
<header>
  <div class="eyebrow">CharaChorder Two · мапа клавіш</div>
  <h1>Що де лежить, і де ще є місце</h1>
  <p class="lede">Схема зібрана з прошивки — <span class="mono">tangent-cc-lib</span>,
  типова розкладка пристрою. Три шари, дві половини, дев'ять стіків на руку,
  чотири напрямки плюс центр. Перемикай шар і мову, щоб побачити, що саме
  друкує кожен слот.</p>
</header>

<div class="bar">
  <div class="seg" id="layers" role="group" aria-label="Шар">
    <button data-l="1" aria-pressed="true">A1 · база</button>
    <button data-l="2" aria-pressed="false">A2 · мізинець назовні</button>
    <button data-l="3" aria-pressed="false">A3 · мізинець вниз</button>
  </div>
  <div class="seg" id="langs" role="group" aria-label="Мова">
    <button data-g="ua" aria-pressed="true">Українська</button>
    <button data-g="en" aria-pressed="false">Англійська</button>
  </div>
</div>

<div class="board" id="board"></div>

<div class="legend">
  <span class="lg"><span class="sq" style="background:var(--letter-bg);border:1px solid var(--letter)"></span>літера</span>
  <span class="lg"><span class="sq" style="background:var(--sym-bg);border:1px solid var(--sym)"></span>символ або цифра</span>
  <span class="lg"><span class="sq" style="border:1px dashed var(--hair)"></span>модифікатор чи системна дія</span>
  <span class="lg"><span class="sq" style="border:1px solid var(--hair)"></span>центр — вхід акорду</span>
  <span class="lg"><span class="sq" style="border:1px dashed var(--free)"></span>порожньо</span>
  <span class="lg"><span class="sq" style="background:var(--free-bg);border:1px solid var(--free)"></span>єдина правка в пристрої</span>
</div>

<section>
  <h2>Як читати</h2>
  <p>Кожен стік — це хрестик з чотирьох напрямків і центру. <b>«Всередину»</b>
  завжди вказує до середини тіла, тому половини дзеркальні: у лівої руки
  «всередину» — це праворуч, у правої — ліворуч. Схема саме так і намальована,
  тож те, що на картинці ближче до центру, ближче до центру й на столі.</p>
  <p>Геометрія розташування стіків умовна — це схема зв'язків, а не креслення
  пристрою. Точні тут призначення, а не міліметри.</p>
</section>

<section>
  <h2>Де насправді є вільне місце</h2>
  <p>Коротка відповідь: на <b>A1 вільного немає жодного слота</b>, і це не
  питання смаку — 33 українські літери просто не вміщаються там, де латиниця
  тримає 26 літер плюс пунктуацію. Усе вільне місце живе на A2 і A3.</p>

  <div class="scroll"><table>
    <thead><tr><th>шар</th><th>зайнято</th><th>чим саме</th><th>що можна забрати</th></tr></thead>
    <tbody>
      <tr>
        <td class="mono">A1</td><td class="n">49 клавіш</td>
        <td>літери, пунктуація, пробіли, модифікатори, миша</td>
        <td>нічого без втрат</td>
      </tr>
      <tr>
        <td class="mono">A2</td><td class="n">42 клавіші</td>
        <td>цифри 0–9 <i>двічі</i>, дужки, <span class="mono">= \ ` </span>, стрілки, миша</td>
        <td>другий комплект цифр — 10 слотів</td>
      </tr>
      <tr>
        <td class="mono">A3</td><td class="n">51 клавіша</td>
        <td>F1–F12 <i>двічі</i>, стрілки, миша, дублі літер</td>
        <td>майже все — це найбільший резерв</td>
      </tr>
    </tbody>
  </table></div>

  <div class="callout">
    <p><b>A3 — це твій склад.</b> Він майже цілком зайнятий F1–F12, продубльованими
    на обидві руки, плюс стрілки й миша. Якщо функціональні клавіші тобі на CC2
    не потрібні щодня, там звільняється більше двадцяти зручних слотів — набагато
    більше, ніж треба будь-якій схемі розміщення символів.</p>
  </div>
</section>

<section>
  <h2>Єдина правка в пристрої</h2>
  <p>На шарі A1 права <span class="mono">index out</span> позначена бурштиновим.
  Це єдиний слот, який український профіль змінює: замість
  <span class="mono">SpaceRight</span> там стає <span class="mono">Backslash</span>,
  а розкладка ОС друкує з нього <b>ю</b>. Лівий пробіл лишається недоторканим.</p>
  <p>У Device Manager шукай дію, підписану просто <kbd>\</kbd>. Саме
  <span class="mono">Backslash</span>, а не <span class="mono">IntlBackslash</span>:
  друга — це 102-га клавіша ISO-клавіатур, і на ANSI-розкладці US її нема де
  намалювати, тож у списку її просто немає.</p>
  <p><span class="mono">\</span> і <span class="mono">|</span> переїжджають на
  AltGr тієї ж клавіші. В українському тексті вони не трапляються, а для коду є
  англійський профіль, якого ця правка не торкається взагалі.</p>
</section>
</div>

<script>
const DATA = __DATA__;
const SW = [
  ['index','middle','ring','little'],
  ['middleMid','ringMid'],
  ['thumbTip','thumbMid','thumbEnd']
];
const NAMES = {index:'index',middle:'middle',ring:'ring',little:'little',
  middleMid:'mid·m',ringMid:'mid·r',thumbTip:'thumb tip',thumbMid:'thumb mid',
  thumbEnd:'thumb end'};
let layer = 1, lang = 'ua';

function rose(half, sw){
  const el = document.createElement('div');
  el.className = 'sw';
  const nm = document.createElement('div');
  nm.className = 'nm'; nm.textContent = NAMES[sw];
  el.appendChild(nm);
  const g = document.createElement('div');
  g.className = 'rose';
  // mirrored: "in" always points at the body midline
  const side = half === 'L' ? ['out','in'] : ['in','out'];
  const plan = [null,'north',null, side[0],'down',side[1], null,'south',null];
  for (const d of plan){
    const c = document.createElement('div');
    if (!d){ c.className = 'c gap'; g.appendChild(c); continue; }
    const k = DATA[layer + half + sw + d] || {k:'free',ua:'',en:''};
    const txt = (lang === 'ua' ? k.ua : k.en) || '';
    c.className = 'c ' + (k.k === 'ukr' && lang === 'en' ? 'sym' : k.k)
                + (txt.length > 2 ? ' sm' : '');
    c.textContent = txt;
    if (k.note) c.title = half + ' ' + sw + ' ' + d + ' — ' + k.note;
    g.appendChild(c);
  }
  el.appendChild(g);
  return el;
}

function draw(){
  const board = document.getElementById('board');
  board.textContent = '';
  for (const half of ['L','R']){
    const h = document.createElement('div');
    h.className = 'hand';
    const t = document.createElement('div');
    t.className = 'eyebrow';
    t.textContent = half === 'L' ? 'ліва половина' : 'права половина';
    h.appendChild(t);
    for (const row of SW){
      const r = document.createElement('div');
      r.className = 'row';
      const order = half === 'L' ? [...row].reverse() : row;
      for (const sw of order) r.appendChild(rose(half, sw));
      h.appendChild(r);
    }
    board.appendChild(h);
  }
}

function wire(id, attr, set){
  document.getElementById(id).addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    for (const x of e.currentTarget.querySelectorAll('button'))
      x.setAttribute('aria-pressed', String(x === b));
    set(b.dataset[attr]);
    draw();
  });
}
wire('layers', 'l', v => layer = +v);
wire('langs', 'g', v => lang = v);
draw();
</script>
'''

if __name__ == '__main__':
    html = TEMPLATE.replace('__DATA__', json.dumps(build(), ensure_ascii=False))
    out = HERE / 'cc2-map.html'
    out.write_text(html, encoding='utf-8')
    print('written', out, len(html), 'bytes')
