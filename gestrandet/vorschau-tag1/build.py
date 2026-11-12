import json, re, subprocess
W = json.load(open('/home/user/videos/gestrandet/tag1/voice-words.json'))
idx = dict(okay=0, das=6, tag=11, mein=15, paddel=18, ohne=19, boot=20, kokos=23, kevin=25, regel=26, jeder=28, follower=29, aktuell=36, einer=37, plus=38, und=40, da=41, sturm=45, huette=46, oder=50, du=57, morgen=64, kevinEnd=67)
E = {k: W[i]['s'] for k, i in idx.items()}
E['dur'] = round(W[-1]['e'] + 1.4, 2)
GOLD = {"kreuzfahrt", "kreuzfahrt.", "kevin.", "follower", "überlebender", "hütte", "feuer,", "kokosnuss", "folg,", "paddel."}
RED = {"allein.", "ohne", "boot.", "sturm.", "sturm?", "gestrandet."}
chunks, cur = [], []
for w in W:
    cur.append(w); txt = " ".join(x["w"] for x in cur)
    if re.search(r"[.!?:,]$", w["w"]) or len(cur) >= 3 or len(txt) >= 11: chunks.append(cur); cur = []
if cur: chunks.append(cur)
caps = []
for i, c in enumerate(chunks):
    st = c[0]["s"]; en = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else c[-1]["e"] + 0.9
    en = min(en, c[-1]["e"] + 0.6)
    caps.append({"s": round(st, 3), "e": round(en, 3), "w": [[{"eins.": "1."}.get(w["w"], w["w"]).upper(), "g" if w["w"].lower() in GOLD else "r" if w["w"].lower() in RED else ""] for w in c]})
s = open('template.html').read().replace('__EVENTS__', json.dumps(E)).replace('__CAPS__', json.dumps(caps, ensure_ascii=False, separators=(",", ":")))
open('index.html', 'w').write(s)
open('render.html', 'w').write('<meta charset="utf-8">\n' + s)
# audio mix
A = "/home/user/videos/gestrandet/audio/norm"; DUR = E['dur']
SFX = [("wave", 0.0, 0.8), ("seagull", 0.6, 0.35), ("whoosh", E['das'] + 0.2, 0.45), ("knock", E['tag'], 0.5), ("whoosh", E['mein'], 0.35),
       ("pop", E['paddel'], 0.5), ("pop", E['ohne'], 0.5), ("sad", E['boot'], 0.35), ("knock", E['kevin'], 0.6), ("pop", E['jeder'] + 0.1, 0.5),
       ("pop", E['aktuell'], 0.45), ("sad", E['plus'] + 0.4, 0.4), ("thunder", E['da'], 0.55), ("thunder", E['sturm'] - 0.05, 0.75),
       ("build", E['huette'], 0.5), ("fire", E['oder'], 0.5), ("knock", E['kevinEnd'], 0.6), ("seagull", E['du'], 0.25)]
inputs = ["-i", "/home/user/videos/gestrandet/tag1/voice.mp3", "-i", f"{A}/music.wav"]
fl = [f"[0]apad=whole_dur={DUR},asplit=2[v][vk]", f"[1]aloop=loop=1:size=2e6,volume=0.55,atrim=0:{DUR},afade=t=in:d=0.3,afade=t=out:st={DUR-1.2:.2f}:d=1.2[mr]", "[mr][vk]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=350[m]"]
labels = ["[v]", "[m]"]
for k, (fx, t, vol) in enumerate(SFX):
    inputs += ["-i", f"{A}/{fx}.wav"]; ms = int(max(0, t) * 1000)
    fl.append(f"[{k+2}]volume={vol},adelay={ms}|{ms}[s{k}]"); labels.append(f"[s{k}]")
fl.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{DUR},alimiter=limit=0.95[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "128k", "audio/tag1.mp3"], check=True)
print(E)
