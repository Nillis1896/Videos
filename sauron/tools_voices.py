# Speeds up each voice, re-times its words, mixes it with dark music + SFX,
# and writes the voice data the preview page needs.
import json, re, subprocess
A = "assets/audio"
VOICES = [
  ("bartholomeus", "Bartholomeus", "maximal böse"),
]
TARGET_END = 29.8          # where the last word should end after speeding up
TAIL = 1.45                # seconds after the last word (as in the original cut)
adam = json.load(open(f"{A}/voice-words.json"))
ADAM_END = 36.05
DISPLAY = {"eins:": "1:", "O-G-Orks!": "OG-ORKS!"}
GOLD = {"ork-armee","ork!","orks","og-orks!","top-kommentar","kommentare!","schmiede","erstes?","mauer","follower"}
RED = {"null.","nacht","elben","elben?","schwert.","rostiges","sauron."}
# SFX placed in the original (Adam) timeline; warped per voice
SFX = [("slam",0.15,0.75),("whoosh",0.0,0.45),("hit",6.1,0.45),("hit",7.4,0.4),("hit",9.6,0.45),("whoosh",12.8,0.4),
       ("sting",14.4,0.45),("hit",15.3,0.45),("horn",18.3,0.45),("whoosh",21.1,0.4),("hit",23.95,0.45),("hit",27.3,0.45),
       ("forge",29.6,0.45),("forge",31.2,0.45),("hit",33.0,0.45)]

def caps_for(words):
    chunks, cur = [], []
    for w in words:
        cur.append(w); txt = " ".join(x["w"] for x in cur)
        if re.search(r"[.!?:,]$", w["w"]) or len(cur) >= 3 or len(txt) >= 11: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        s = c[0]["s"]; e = chunks[i+1][0]["s"] if i+1 < len(chunks) else c[-1]["e"] + 0.8
        e = min(e, c[-1]["e"] + 0.6)
        out.append({"s": round(s,3), "e": round(e,3), "w": [[DISPLAY.get(w["w"], w["w"]).upper(), "g" if w["w"].lower() in GOLD else "r" if w["w"].lower() in RED else ""] for w in c]})
    return out


import os
os.makedirs(f"{A}/dark/norm", exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{A}/dark/music.mp3","-af","dynaudnorm=f=400:g=31:p=0.9:m=20:s=12,loudnorm=I=-20:TP=-2:LRA=4","-ar","44100",f"{A}/dark/norm/music.wav"], check=True)
for fx in ["hit","whoosh","horn","forge","sting","slam"]:
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{A}/dark/{fx}.mp3","-af","loudnorm=I=-18:TP=-3","-ar","44100",f"{A}/dark/norm/{fx}.wav"], check=True)

data = []
for vid, name, desc in VOICES:
    words = json.load(open(f"{A}/voices/{vid}.json"))
    assert len(words) == len(adam), vid
    f = words[-1]["e"] / TARGET_END
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{A}/voices/{vid}.mp3","-filter:a",f"atempo={f:.4f},loudnorm=I=-15:TP=-1.5","-b:a","128k",f"{A}/voices/{vid}_fast.mp3"], check=True)
    fw = [{"w": w["w"], "s": w["s"]/f, "e": w["e"]/f} for w in words]
    dur = round(fw[-1]["e"] + TAIL, 2)
    anchors = [[0.0, 0.0]] + [[round(a["s"],3), round(b["s"],3)] for a, b in zip(adam, fw)] + [[ADAM_END, dur]]
    def warp(t):
        for (a0,b0),(a1,b1) in zip(anchors, anchors[1:]):
            if t <= a1: return b0 + (b1-b0) * (t-a0) / max(1e-6, a1-a0)
        return anchors[-1][1]
    inputs = ["-i", f"{A}/voices/{vid}_fast.mp3", "-i", f"{A}/dark/norm/music.wav"]
    fl = [f"[0]apad=whole_dur={dur},asplit=2[v][vk]", f"[1]volume=0.55,atrim=0:{dur},afade=t=in:d=0.3,afade=t=out:st={dur-1.6:.2f}:d=1.6[mr]", "[mr][vk]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=350[m]"]
    labels = ["[v]", "[m]"]
    for k, (fx, t, vol) in enumerate(SFX):
        inputs += ["-i", f"{A}/dark/norm/{fx}.wav"]
        ms = int(warp(t) * 1000)
        fl.append(f"[{k+2}]volume={vol},adelay={ms}|{ms}[s{k}]"); labels.append(f"[s{k}]")
    fl.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{dur},alimiter=limit=0.95[out]")
    subprocess.run(["ffmpeg","-v","error","-y",*inputs,"-filter_complex",";".join(fl),"-map","[out]","-c:a","libmp3lame","-b:a","128k",f"../vorschau/audio/{vid}.mp3"], check=True)
    data.append({"id": vid, "name": name, "desc": desc, "src": f"audio/{vid}.mp3", "dur": dur, "anchors": anchors, "caps": caps_for(fw)})
    print(vid, f"tempo x{f:.2f}", "dur", dur)
open("/tmp/claude-0/-home-user-videos/41e50950-5764-5215-88cb-2d4a1d8cb511/scratchpad/voices.json","w").write(json.dumps(data, ensure_ascii=False, separators=(",",":")))
