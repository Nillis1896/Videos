import re, json
src = open('/home/user/videos/vorschau-tag2/index.html').read()
s = src
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)
def cut(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]

# ---- voice + captions ----
words = json.load(open('/home/user/videos/sauron/tag3/voice-words.json'))
DUR = round(words[-1]['e'] + 1.6, 2)
GOLD = {"wachturm", "feuer!", "charles.", "drache!", "kommentare!", "ja", "drei."}
RED = {"an!", "reiter", "anführer", "fallen.", "an?"}
chunks, cur = [], []
for w in words:
    cur.append(w); txt = " ".join(x["w"] for x in cur)
    if re.search(r"[.!?:,]$", w["w"]) or len(cur) >= 3 or len(txt) >= 11: chunks.append(cur); cur = []
if cur: chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    st = c[0]["s"]; en = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else c[-1]["e"] + 0.8
    en = min(en, c[-1]["e"] + 0.6)
    caps.append({"s": round(st, 3), "e": round(en, 3), "w": [[{"drei.": "3."}.get(w["w"], w["w"]).upper(), "g" if w["w"].lower() in GOLD else "r" if w["w"].lower() in RED else ""] for w in c]})
data = [{"id": "tag3", "name": "Bartholomeus", "desc": "psycho", "src": "audio/tag3.mp3", "dur": DUR, "rh": None, "anchors": [[0, 0], [DUR, DUR]], "caps": caps}]
s = re.sub(r'const VOICES = \[.*?\];\n', lambda m: 'const VOICES = ' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ';\n', s, count=1, flags=re.S)
R('const FEATURED = ["caspar", "Charles", "mb2008", "Travisschoko"];', 'const FEATURED = [];\nconst RIGHT_HAND = "Charles";')
R('const FOLLOWERS = 404;', 'const FOLLOWERS = 470;')
R('<title>Sauron Tag 2</title>', '<title>Sauron Tag 3</title>')
R('<div id="signtitle" class="molten">TAG 2</div>', '<div id="signtitle" class="molten">TAG 3</div>')
R('#sign { top: 90px; visibility: visible; }', '#sign { top: 90px; visibility: hidden; }')

# ---- icons ----
R('  </defs>', '''    <symbol id="i-wt" viewBox="0 0 60 60"><path d="M14 58 L22 22 M46 58 L38 22 M18 44 L42 44" stroke="#c99646" stroke-width="5" stroke-linecap="round"/><rect x="16" y="16" width="28" height="8" fill="#8a5a30" stroke="#0e0c0c" stroke-width="2"/><path d="M12 16 L30 2 L48 16 Z" fill="#a8321e" stroke="#0e0c0c" stroke-width="2"/></symbol>
    <symbol id="i-horse" viewBox="0 0 60 60"><path d="M12 46 L14 30 Q14 22 24 22 L36 22 L44 12 L52 16 L48 22 Q50 26 46 28 L44 30 L44 46 M20 30 L20 46 M38 30 L38 46" stroke="#e8dcc8" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="46" cy="18" r="2" fill="#ff3a1a"/></symbol>
  </defs>''')

# ---- HUD ----
cut('<div id="hud" class="ov">', '<div id="held" class="ov"', '''<div id="hud" class="ov">
          <div class="glowwrap"><div id="hud1" class="plate hplate"><svg><use href="#i-ork"/></svg><div><span id="hudorks" class="num">471</span><span class="lab">ORKS</span></div></div></div>
          <div class="glowwrap"><div id="hud2" class="plate hplate"><svg><use href="#i-wt"/></svg><div><span class="num">1</span><span class="lab">WACHTURM</span></div></div></div>
          <div class="glowwrap" id="hud3wrap"><div id="hud3" class="plate hplate"><svg><use href="#i-horse"/></svg><div><span id="hudreiter" class="num">23</span><span class="lab">REITER</span></div><div id="hud3red"></div></div></div>
        </div>

        ''')

# ---- overlays ----
cut('<div id="held" class="ov"', '<div id="caps"></div>', '''<div id="attack" class="ov" style="top:300px;visibility:visible">
          <div id="attackin" class="rune blood" style="font-size:132px;line-height:1">SIE GREIFEN</div>
          <div id="attackin2" class="rune blood" style="font-size:190px;line-height:1">AN!</div>
        </div>

        <div id="chosen" class="ov" style="top:330px">
          <div class="engrave" style="font-size:34px">IHR HABT GEWÄHLT</div>
          <div class="glowwrap" style="margin-top:14px"><div class="plate badge"><svg width="70" height="70"><use href="#i-wt"/></svg><span class="molten" style="font:900 72px/1 var(--font-rune)">WACHTURM</span></div></div>
        </div>

        <div id="feuer" class="ov" style="top:330px">
          <div id="feuerin" class="rune molten" style="font-size:180px;line-height:1">FEUER!</div>
        </div>

        <div id="rhand" class="ov" style="top:320px">
          <div class="engrave" style="font-size:36px">MEINE RECHTE HAND</div>
          <div class="glowwrap" style="margin-top:12px"><div class="plate" style="padding:18px 50px 22px;text-align:center"><div id="rhname" class="molten" style="font:900 96px/1 var(--font-rune)">CHARLES</div><div class="engrave" style="font-size:30px;margin-top:6px">DER DRACHE</div></div></div>
        </div>

        <div id="sieg" class="ov" style="top:330px">
          <div class="rune molten" style="font-size:200px;line-height:1">SIEG!</div>
        </div>

        <div id="ask" class="ov" style="top:300px">
          <div class="rune outline" style="color:#fff;font-size:76px">GREIFEN WIR AN?</div>
        </div>
        <div id="choice" class="ov">
          <div id="cardA" class="card"><div class="seal" style="font-size:34px">JA</div>
            <svg viewBox="0 0 190 150"><path d="M40 130 L150 20 M60 20 L170 130" stroke="#3a3d48" stroke-width="12" stroke-linecap="round"/><path d="M150 20 L168 14 L162 32 Z M170 130 L176 112 L158 118 Z" fill="#c0c4cc"/></svg>
            <div class="ct" style="font-size:50px">ANGRIFF!</div><div class="cs">AUF DIE ELBEN</div></div>
          <div id="oder" class="outline" style="color:#fff">ODER</div>
          <div id="cardB" class="card"><div class="seal" style="font-size:28px">NEIN</div>
            <svg viewBox="0 0 190 150"><use href="#i-wall" x="25" y="5" width="140" height="140"/></svg>
            <div class="ct" style="font-size:46px">AUFRÜSTEN</div><div class="cs">ERST STÄRKER WERDEN</div></div>
        </div>
        <div id="share" class="ov" style="top:1035px">
          <div class="glowwrap"><div class="plate" style="padding:12px 30px 14px"><span class="engrave" style="font-size:30px;color:#ffd27a">📲 SCHICK DAS DEINEM GENERAL</span></div></div>
        </div>
        <div id="flash"></div>

        ''')
R('  .cap { position: absolute;', '''  #flash { position: absolute; inset: 0; background: radial-gradient(circle at 50% 45%, #fff6d0 0%, #ffb02a 35%, rgba(255,80,0,.6) 70%, rgba(120,20,0,0) 100%); opacity: 0; pointer-events: none; z-index: 5; }
  #choice { top: 430px !important; }
  .cap { position: absolute;''')

# ---- timeline ----
cut('  // HUD\n', '  // captions\n', r'''  // frame 0: the attack banner is already on screen
  tl.fromTo("#attackin, #attackin2", { x: 0 }, { x: 8, duration: 0.05, yoyo: true, repeat: 13, ease: "none" }, 0.05);
  tl.fromTo("#attackin2", { scale: 1 }, { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1 }, 0.72);
  tl.to("#attack", { opacity: 0, scale: 0.7, duration: 0.15 }, 1.45);
  tl.set("#attack", { visibility: "hidden" }, 1.6);
  // TAG 3 sign slams briefly
  tl.set("#sign", { visibility: "visible" }, 1.6);
  tl.fromTo("#signwrap", { y: -700 }, { y: 0, duration: 0.25, ease: "power4.in" }, 1.6);
  tl.fromTo("#shake", { x: 0, y: 0 }, { keyframes: [{ x: -12, y: 8 }, { x: 10, y: -6 }, { x: -6, y: 4 }, { x: 0, y: 0 }], duration: 0.3, ease: "none" }, 1.85);
  tl.to("#signwrap", { y: -900, duration: 0.3, ease: "power3.in" }, 2.75);
  tl.set("#sign", { visibility: "hidden" }, 3.1);
  // HUD
  show("#hud", 1.62, 99);
  tl.fromTo("#hud .glowwrap", { y: -140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.07 }, 1.62);
  tl.to("#hud3red", { opacity: 1, duration: 0.2 }, 2.7);
  // your vote
  show("#chosen", 4.4, 7.3); pop("#chosen", 4.4);
  tl.to("#hud2", { scale: 1.2, duration: 0.15, yoyo: true, repeat: 1 }, 5.2);
  out("#chosen", 7.1);
  // FIRE
  show("#feuer", 8.3, 9.3);
  tl.fromTo("#feuerin", { scale: 2.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.18, ease: "power3.out" }, 8.3);
  tl.fromTo("#shake", { x: 0, y: 0 }, { keyframes: [{ x: -10, y: 6 }, { x: 8, y: -5 }, { x: -4, y: 3 }, { x: 0, y: 0 }], duration: 0.3, ease: "none" }, 8.35);
  out("#feuer", 9.1);
  // right hand
  show("#rhand", 16.85, 18.5);
  tl.fromTo("#rhand", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }, 16.85);
  out("#rhand", 18.3);
  // the blast
  tl.fromTo("#flash", { opacity: 0 }, { keyframes: [{ opacity: 0.95, duration: 0.08 }, { opacity: 0, duration: 0.5 }], ease: "none" }, 18.6);
  tl.fromTo("#shake", { x: 0, y: 0 }, { keyframes: [{ x: -18, y: 12 }, { x: 14, y: -10 }, { x: -9, y: 7 }, { x: 5, y: -3 }, { x: 0, y: 0 }], duration: 0.45, ease: "none" }, 18.62);
  tl.to("#hud3", { scale: 1.25, duration: 0.15, yoyo: true, repeat: 1 }, 18.65);
  // victory
  show("#sieg", 18.85, 20.15); pop("#sieg", 18.85); out("#sieg", 19.95);
  // question + cards
  show("#ask", 20.2, 99); pop("#ask", 20.2);
  tl.fromTo("#ask .rune", { rotation: 0 }, { rotation: 3, duration: 0.1, yoyo: true, repeat: 3 }, 20.9);
  show("#choice", 21.7, 99);
  tl.fromTo("#cardA", { y: -900, rotation: -12 }, { y: 0, rotation: -4, duration: 0.45, ease: "back.out(1.5)" }, 21.75);
  tl.fromTo("#cardB", { y: -900, rotation: 12, opacity: 0 }, { y: 0, rotation: 4, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }, 22.25);
  tl.fromTo("#oder", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }, 22.3);
  show("#share", 23.0, 99);
  tl.fromTo("#share", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 23.0);
''')
R('gsap.set(["#platzin", ".ftin"], { xPercent: -50, yPercent: -100 });', 'gsap.set([".ftin"], { xPercent: -50, yPercent: -100 });')
R('  gsap.set("#stage *", { clearProps: "transform,opacity,visibility,filter,strokeDashoffset" });', '  gsap.set("#stage *", { clearProps: "transform,opacity,visibility,filter,strokeDashoffset" });\n  gsap.set("#attack", { visibility: "visible" });')
open('index.html', 'w').write(s); print('stage1 ok', DUR)
