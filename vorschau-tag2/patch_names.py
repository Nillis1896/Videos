s = open('index.html').read()
def cut(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]
def R(a, b):
    global s
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b)

R('const NEW_ORKS = 12;   // neue Follower seit Tag 1 – hier die echte Zahl eintragen',
  '''// neue Follower seit Tag 1: Name und Rolle (Rolle bestimmt das Aussehen)
const RECRUITS = [
  ["Lucas", "Hexenkönig", "wraith"], ["Timon", "Hexenkönig", "wraith"], ["Leon", "Saruman", "white"], ["RBL", "Riese", "giant"],
  ["Raptor", "Lurtz", "uruk"], ["Pippo", "Istari", "grey"], ["Tim", "Wikinger", "viking"], ["Konstantin", "General", "general"]
];
const NEW_ORKS = RECRUITS.length;''')

# roll call overlay replaces the "+12 neue Orks" badge
cut('<div id="neworks" class="ov" style="top:320px">', '<div id="food" class="ov"', '''<div id="neworks" class="ov" style="top:310px">
          <div class="rune" style="font-size:72px"><span id="neworksnum" class="molten">+8</span> <span class="outline" style="color:#fff">NEUE KRIEGER</span></div>
          <div id="roll" class="plate"><div id="rolllist"></div></div>
        </div>

        ''')
R('  .cap { position: absolute;', '''  #roll { margin-top: 18px; width: 640px; padding: 22px 34px 24px; }
  #rolllist { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 26px; }
  .rl { font: 900 30px/1.15 var(--font-engrave); color: #e9dfcf; text-shadow: 0 2px 0 #000; }
  .rl small { display: block; font: 700 21px/1.2 var(--font-engrave); letter-spacing: .16em; color: var(--gold); }
  .cap { position: absolute;''')

# characters instead of generic orcs
cut('// orcs\nconst orcs = [];', '// riders on the ridge', r'''// recruits: one figure per new follower, styled by role
const orcs = [];
{
  const M = (c, o) => std(c, { flatShading: false, ...o });
  const SLOTS = [[-1.7, -0.4], [1.8, -0.5], [-2.7, 0.5], [-3.7, -1.7], [2.8, 0.4], [-1.2, 1.0], [1.3, 1.0], [3.5, -1.1], [-2.2, -1.9], [2.3, -2.0], [0.6, -2.4], [-0.7, -2.3], [-3.5, 1.1], [3.7, 1.2]];
  const LOOK = {
    wraith:  { skin: 0x111014, body: 0x141218, robe: 0x0e0d10, head: "crown", eyes: 0x9fd8ff, weapon: "sword", scale: 1.15 },
    white:   { skin: 0xd8c2a8, body: 0xe8e6e0, robe: 0xf2f0ea, head: "hair", beard: 0xf0f0f0, weapon: "staffdark", scale: 1.1 },
    giant:   { skin: 0x7a6a58, body: 0x4a3a2a, head: "bald", eyes: 0xff6a1a, weapon: "club", scale: 1.75 },
    uruk:    { skin: 0x2e2a24, body: 0x1c1814, head: "uruk", eyes: 0xff3a1a, weapon: "sword", scale: 1.15 },
    grey:    { skin: 0xd8c2a8, body: 0x7a7a80, robe: 0x8a8a90, head: "hat", beard: 0xcfcfcf, weapon: "staffglow", scale: 1.1 },
    viking:  { skin: 0xd8b090, body: 0x5a3a24, head: "horns", beard: 0xc0602a, weapon: "axe", scale: 1.05 },
    general: { skin: 0x4f7a2e, body: 0x2a2b33, head: "plume", eyes: 0xff3a1a, weapon: "sword", cape: true, scale: 1.12 }
  };
  RECRUITS.forEach(([name, role, kind], i) => {
    const L = LOOK[kind] || LOOK.uruk, [x, z] = SLOTS[i];
    const o = new THREE.Group(), body = new THREE.Group(); o.add(body);
    const skin = M(L.skin), cloth = M(L.body), dark = M(0x1c1612), wood = M(0x5a3a1a), steel = metal(0x8a8c94);
    if (L.robe) { mesh(new THREE.CylinderGeometry(0.17, 0.32, 0.8, 10), M(L.robe), 0, 0.4, 0, body); }
    else { [-1, 1].forEach(s => mesh(new THREE.CylinderGeometry(0.07, 0.06, 0.34, 6), dark, s * 0.1, 0.17, 0, body)); mesh(new THREE.CylinderGeometry(0.2, 0.24, 0.42, 8), cloth, 0, 0.55, 0, body); }
    mesh(new THREE.CylinderGeometry(0.21, 0.21, 0.08, 8), cloth, 0, 0.74, 0, body);
    [-1, 1].forEach(s => { const a = mesh(new THREE.CylinderGeometry(0.06, 0.05, 0.38, 6), L.robe ? M(L.robe) : skin, s * 0.27, 0.6, 0, body); a.rotation.z = s * 0.25; });
    if (L.cape) { const c = mesh(new THREE.CylinderGeometry(0.22, 0.38, 0.7, 10, 1, true, Math.PI * 0.6, Math.PI * 0.8), M(0x8a1010, { side: THREE.DoubleSide }), 0, 0.5, -0.04, body); }
    const head = mesh(new THREE.SphereGeometry(0.16, 12, 10), kind === "wraith" ? M(0x050506) : skin, 0, 0.93, 0.02, body);
    if (L.eyes) [-1, 1].forEach(s => mesh(new THREE.SphereGeometry(0.024, 6, 6), glow(L.eyes), s * 0.06, 0.95, 0.16, body));
    else [-1, 1].forEach(s => mesh(new THREE.SphereGeometry(0.018, 6, 6), M(0x1a1a1a), s * 0.055, 0.96, 0.15, body));
    if (L.beard) { const b = mesh(new THREE.ConeGeometry(0.11, 0.3, 8), M(L.beard), 0, 0.78, 0.1, body); b.rotation.x = Math.PI; }
    if (kind === "uruk" || kind === "giant" || kind === "general") [-1, 1].forEach(s => { const e = mesh(new THREE.ConeGeometry(0.045, 0.18, 4), skin, s * 0.19, 0.98, 0, body); e.rotation.z = -s * 1.2; });
    if (kind === "uruk") { const hand = mesh(new THREE.CircleGeometry(0.07, 5), M(0xf4f4f4), 0, 0.93, 0.165, body); }
    if (L.head === "crown") { mesh(new THREE.ConeGeometry(0.24, 0.5, 10, 1, true), M(0x0e0d10, { side: THREE.DoubleSide }), 0, 1.02, -0.02, body); for (let k = 0; k < 6; k++) { const a = k / 6 * Math.PI * 2; mesh(new THREE.ConeGeometry(0.025, 0.2, 4), steel, Math.sin(a) * 0.15, 1.18, Math.cos(a) * 0.15, body); } }
    if (L.head === "hat") { mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.02, 14), M(0x7a7a80), 0, 1.06, 0, body); const h = mesh(new THREE.ConeGeometry(0.15, 0.5, 10), M(0x7a7a80), 0, 1.3, -0.03, body); h.rotation.x = -0.15; }
    if (L.head === "hair") { mesh(new THREE.SphereGeometry(0.17, 10, 8, 0, Math.PI * 2, 0, Math.PI / 2), M(0xf0f0f0), 0, 0.95, -0.02, body); }
    if (L.head === "horns") { mesh(new THREE.SphereGeometry(0.17, 10, 8, 0, Math.PI * 2, 0, Math.PI / 2), steel, 0, 0.96, 0, body); [-1, 1].forEach(s => { const hn = mesh(new THREE.ConeGeometry(0.04, 0.22, 6), M(0xeee2c8), s * 0.18, 1.08, 0, body); hn.rotation.z = -s * 0.7; }); }
    if (L.head === "plume") { mesh(new THREE.SphereGeometry(0.175, 10, 8, 0, Math.PI * 2, 0, Math.PI / 2), steel, 0, 0.96, 0, body); const pl = mesh(new THREE.BoxGeometry(0.04, 0.12, 0.3), M(0xc01818), 0, 1.15, -0.04, body); }
    const w = new THREE.Group(); w.position.set(0.33, 0.42, 0.06); body.add(w);
    if (L.weapon === "staffdark" || L.weapon === "staffglow") { mesh(new THREE.CylinderGeometry(0.02, 0.025, 1.3, 6), L.weapon === "staffdark" ? M(0x111111) : wood, 0, 0.4, 0, w); mesh(new THREE.SphereGeometry(0.05, 8, 6), L.weapon === "staffglow" ? glow(0xeaf4ff) : M(0x222222), 0, 1.06, 0, w); }
    else if (L.weapon === "axe") { w.rotation.z = -0.3; mesh(new THREE.CylinderGeometry(0.025, 0.03, 0.6, 6), wood, 0, 0.3, 0, w); mesh(new THREE.BoxGeometry(0.02, 0.16, 0.18), steel, 0, 0.58, 0.07, w); const sh = mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.04, 12), M(0x8a2a1a), -0.62, 0.15, 0.05, w); sh.rotation.x = Math.PI / 2; }
    else if (L.weapon === "club") { w.rotation.z = -0.4; mesh(new THREE.CylinderGeometry(0.04, 0.08, 0.7, 6), wood, 0, 0.35, 0, w); mesh(new THREE.DodecahedronGeometry(0.12, 0), wood, 0, 0.72, 0, w); }
    else { w.rotation.z = -0.25; mesh(new THREE.BoxGeometry(0.04, 0.55, 0.015), steel, 0, 0.36, 0, w); mesh(new THREE.BoxGeometry(0.16, 0.03, 0.04), M(0x5a4a3a), 0, 0.08, 0, w); }
    o.scale.setScalar(L.scale);
    o.userData = { slot: new THREE.Vector3(x, 0, z), start: new THREE.Vector3(x * 0.3, 0, -10 - i * 0.5), body };
    o.rotation.y = -x * 0.06; o.visible = false; scene.add(o); orcs.push(o);
  });
}
''')

# timeline: fill the roll call
R('  document.getElementById("neworksnum").textContent = "+" + NEW_ORKS;\n  show("#neworks", 8.6, 10.0); pop("#neworks", 8.6);\n  tl.fromTo("#neworksnum", { scale: 1 }, { scale: 1.2, duration: 0.15, yoyo: true, repeat: 1 }, 9.4);\n  out("#neworks", 9.8);',
  '''  document.getElementById("neworksnum").textContent = "+" + NEW_ORKS;
  const rl = document.getElementById("rolllist"); rl.textContent = "";
  RECRUITS.forEach(([name, role]) => { const d = document.createElement("div"); d.className = "rl"; d.textContent = name; const sm = document.createElement("small"); sm.textContent = role.toUpperCase(); d.append(sm); rl.append(d); });
  show("#neworks", 8.6, 11.3); pop("#neworks", 8.6);
  tl.fromTo("#rolllist .rl", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "power2.out", stagger: 0.16 }, 8.8);
  tl.fromTo("#neworksnum", { scale: 1 }, { scale: 1.2, duration: 0.15, yoyo: true, repeat: 1 }, 9.4);
  out("#neworks", 11.1);''')
open('index.html', 'w').write(s); print('ok')
