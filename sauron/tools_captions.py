# Builds compositions/captions.html from assets/audio/voice-words.json
import json, re, html
words = json.load(open("assets/audio/voice-words.json"))
DISPLAY = {"eins:": "1:", "O-G-Orks!": "OG-ORKS!"}
GREEN = {"ork-armee", "ork!", "orks", "og-orks!", "top-kommentar", "kommentare!", "schmiede", "erstes?", "mauer", "follower"}
RED = {"null.", "nacht", "elben", "elben?", "schwert.", "rostiges", "sauron."}
chunks, cur = [], []
for w in words:
    cur.append(w)
    txt = " ".join(x["w"] for x in cur)
    if re.search(r"[.!?:,]$", w["w"]) or len(cur) >= 3 or len(txt) >= 11:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)
# merge one-letter-ish leftovers is unnecessary; build html
items = []
for i, c in enumerate(chunks):
    s = c[0]["s"]
    e = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else c[-1]["e"] + 0.8
    if e - c[-1]["e"] > 0.6: e = c[-1]["e"] + 0.6
    spans = []
    for w in c:
        t = DISPLAY.get(w["w"], w["w"]).upper()
        k = w["w"].lower()
        cls = "cap-g" if k in GREEN else "cap-r" if k in RED else ""
        spans.append(f'<span class="{cls}">{html.escape(t)}</span>' if cls else html.escape(t))
    items.append((i, round(s, 2), round(e - s, 2), " ".join(spans)))
rows = "\n".join(
    f'    <div id="cap-{i}" class="cap clip" data-start="{s}" data-duration="{d}" data-track-index="1"><div class="cap-in">{t}</div></div>'
    for i, s, d, t in items)
anims = "\n".join(f'    tl.fromTo("#cap-{i} .cap-in", {{ scale: 0.55, y: 30 }}, {{ scale: 1, y: 0, duration: 0.14, ease: "back.out(2.6)" }}, {s});' for i, s, d, t in items)
open("compositions/captions.html", "w").write(f'''<template>
  <style>
    @font-face {{ font-family: "LilitaOne"; src: url("assets/fonts/LilitaOne.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 60px; right: 60px; top: 1180px; text-align: center; }}
    .cap-in {{ display: inline-block; font-family: "LilitaOne", sans-serif; font-size: 92px; line-height: 1.05; color: #fff;
      text-shadow: 5px 5px 0 #141414, -5px 5px 0 #141414, 5px -5px 0 #141414, -5px -5px 0 #141414, 0 7px 0 #141414, 0 -7px 0 #141414, 7px 0 0 #141414, -7px 0 0 #141414, 0 14px 0 rgba(0,0,0,.4); }}
    .cap-g {{ color: #8ef04a; }}
    .cap-r {{ color: #ff3b3b; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{rows}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{anims}
    window.__timelines["captions"] = tl;
  </script>
</template>
''')
print(len(items), "caption groups")
for i, s, d, t in items: print(s, d, re.sub("<[^>]+>", "", t))
