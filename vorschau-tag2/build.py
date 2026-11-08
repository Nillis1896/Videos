import re
src = open('/home/user/videos/vorschau/index.html').read()
voices = open('/tmp/claude-0/-home-user-videos/41e50950-5764-5215-88cb-2d4a1d8cb511/scratchpad/voices_tag2.json').read()
s = src
def cut(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + (s[j:] if keep_b else s[j+len(b):])
def R(a, b):
    global s
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b)

s = re.sub(r'const VOICES = \[.*?\];\n', lambda m: 'const VOICES = ' + voices + ';\nconst NEW_ORKS = 12;   // neue Follower seit Tag 1 – hier die echte Zahl eintragen\n', s, count=1, flags=re.S)
R('<title>Sauron Tag 1</title>', '<title>Sauron Tag 2</title>')
R('<div id="signtitle" class="molten">TAG 1</div>', '<div id="signtitle" class="molten">TAG 2</div>')
R('  </defs>', '''    <symbol id="i-food" viewBox="0 0 60 60"><path d="M22 38 C10 34 8 18 18 10 C28 2 44 8 46 20 C48 30 40 38 30 38 Z" fill="#b5652a" stroke="#0e0c0c" stroke-width="3"/><path d="M26 36 L16 50" stroke="#f2ead8" stroke-width="7" stroke-linecap="round"/><circle cx="14" cy="52" r="4" fill="#f2ead8" stroke="#0e0c0c" stroke-width="2"/><circle cx="19" cy="55" r="4" fill="#f2ead8" stroke="#0e0c0c" stroke-width="2"/></symbol>
    <symbol id="i-pig" viewBox="0 0 190 150"><path d="M30 40 L60 20 L100 30 L140 22 L170 50 L170 110 L30 110 Z" fill="#6b4a2a" stroke="#140f0f" stroke-width="5"/><ellipse cx="100" cy="92" rx="52" ry="34" fill="#f2a0a0" stroke="#140f0f" stroke-width="5"/><ellipse cx="146" cy="86" rx="16" ry="12" fill="#e57f80" stroke="#140f0f" stroke-width="4"/><circle cx="141" cy="86" r="3" fill="#140f0f"/><circle cx="151" cy="86" r="3" fill="#140f0f"/><path d="M70 122 L70 136 M90 124 L90 138 M112 124 L112 138 M132 122 L132 136" stroke="#140f0f" stroke-width="7" stroke-linecap="round"/></symbol>
    <symbol id="i-tower" viewBox="0 0 190 150"><path d="M60 146 L76 40 M130 146 L114 40 M70 100 L120 100 M66 128 L124 128" stroke="#6b4a2a" stroke-width="9" stroke-linecap="round"/><rect x="58" y="34" width="74" height="16" fill="#8a5a30" stroke="#140f0f" stroke-width="4"/><path d="M52 34 L95 4 L138 34 Z" fill="#7a2a1a" stroke="#140f0f" stroke-width="4"/><path d="M150 30 Q170 60 150 90" stroke="#3a2a1a" stroke-width="5" fill="none"/><path d="M150 30 L150 90" stroke="#ddd" stroke-width="2"/><path d="M118 60 L176 60" stroke="#ccc" stroke-width="3"/><path d="M176 60 L168 55 L168 65 Z" fill="#ccc"/></symbol>
  </defs>''')

# HUD: Orks (counts up), Mauer 1, Essen 0
cut('<div id="hud" class="ov">', '<div id="follow1" class="ov">', '''<div id="hud" class="ov">
          <div class="glowwrap"><div id="hud1" class="plate hplate"><svg><use href="#i-ork"/></svg><div><span id="hudorks" class="num">1</span><span class="lab">ORKS</span></div></div></div>
          <div class="glowwrap"><div id="hud2" class="plate hplate"><svg><use href="#i-wall"/></svg><div><span class="num">1</span><span class="lab">MAUER</span></div></div></div>
          <div class="glowwrap" id="hud3wrap"><div id="hud3" class="plate hplate"><svg><use href="#i-food"/></svg><div><span class="num">0</span><span class="lab">ESSEN</span></div><div id="hud3red"></div></div></div>
        </div>

        ''')
R('#hud2red { position: absolute;', '#hud3red { position: absolute;')

# Overlays for day 2
cut('<div id="follow1" class="ov">', '<div id="caps"></div>', '''<div id="held" class="ov" style="top:330px">
          <div class="rune outline" style="color:#fff">SIE HAT</div>
          <div class="rune molten" style="font-size:104px">GEHALTEN!</div>
        </div>

        <div id="follow1" class="ov">
          <div class="fav"><img class="avatar" alt=""><div class="fplus"><svg viewBox="0 0 40 40"><path d="M20 8 V32 M8 20 H32" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg><div class="fcheck"><svg viewBox="0 0 40 40"><path d="M9 21 L17 29 L31 12" stroke="#fe2c55" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
            <svg class="fhand"><use href="#i-hand"/></svg></div>
        </div>

        <div id="neworks" class="ov" style="top:320px">
          <div id="neworksnum" class="bignum molten">+12</div>
          <div class="glowwrap"><div class="plate badge"><svg width="60" height="60"><use href="#i-ork"/></svg><span class="engrave">NEUE ORKS</span></div></div>
        </div>

        <div id="food" class="ov" style="top:330px">
          <div class="glowwrap red"><div class="plate badge"><svg width="60" height="60"><use href="#i-food"/></svg><span class="engrave" style="color:#ffb0a0">ESSEN: 0</span></div></div>
          <div class="rune" style="font-size:58px;margin-top:18px"><span class="outline" style="color:#fff">DIE ORKS HABEN </span><span class="blood">HUNGER</span></div>
        </div>

        <div id="night" class="ov" style="top:330px">
          <div class="rune outline" style="color:#fff">MORGEN NACHT</div>
          <div id="nightred" class="rune blood">KOMMEN DIE REITER</div>
        </div>

        <div id="follow2" class="ov">
          <div class="fav"><img class="avatar" alt=""><div class="fplus"><svg viewBox="0 0 40 40"><path d="M20 8 V32 M8 20 H32" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg><div class="fcheck"><svg viewBox="0 0 40 40"><path d="M9 21 L17 29 L31 12" stroke="#fe2c55" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div></div>
          <div class="ftbtn">Folgen<div class="done"><svg width="44" height="44" viewBox="0 0 40 40"><path d="M9 21 L17 29 L31 12" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>Gefolgt</div><svg class="fhand" style="left:70%;top:40%"><use href="#i-hand"/></svg></div>
        </div>

        <div id="platz" class="ov" style="top:0;left:0;width:auto"><div id="platzin"><div class="glowwrap"><div class="plate tag" style="font-size:34px">DEIN PLATZ</div></div><div class="tagarrow"></div></div></div>

        <div id="comment" class="ov">
          <div id="ccard"><img class="avatar" alt=""><div style="min-width:0"><div class="cmeta">dein.name <span class="ctag">Top-Kommentar</span></div><div class="ctext">das bauen wir! 🔨</div><div class="cmeta" style="margin-top:6px">gerade eben · Antworten</div></div><div class="clikes"><svg width="44" height="44" viewBox="0 0 24 24"><path d="M12 21 L10.5 19.6 C5 14.6 2 11.9 2 8.5 C2 5.7 4.2 3.5 7 3.5 C8.6 3.5 10.1 4.3 12 6 C13.9 4.3 15.4 3.5 17 3.5 C19.8 3.5 22 5.7 22 8.5 C22 11.9 19 14.6 13.5 19.6 Z" fill="#fe2c55"/></svg><div>999+</div></div></div>
          <div id="wirbauen" class="rune" style="font-size:66px;margin-top:24px"><span class="outline" style="color:#fff">= </span><span class="molten">WIR BAUEN ES</span></div>
        </div>

        <div id="choice" class="ov">
          <div id="cardA" class="card"><div class="seal">A</div>
            <svg viewBox="0 0 190 150"><use href="#i-pig"/></svg>
            <div class="ct">STALL</div><div class="cs">FÜR ESSEN</div></div>
          <div id="oder" class="outline" style="color:#fff">ODER</div>
          <div id="cardB" class="card"><div class="seal">B</div>
            <svg viewBox="0 0 190 150"><use href="#i-tower"/></svg>
            <div class="ct" style="font-size:46px">WACHTURM</div><div class="cs">GEGEN DIE REITER</div></div>
        </div>

        <div id="ask" class="ov" style="top:330px">
          <div class="rune outline" style="color:#fff">BAUEN WIR:</div>
          <div id="askq" class="bignum molten" style="font-size:170px">???</div>
        </div>

        ''')

# 3D: built wall with arrows, stall, watchtower, orcs, riders
cut('// ---------- forge (option A) and wall (option B) ----------', '// Embers + ash', r'''// ---------- day 2 set: the wall stands, new orcs, riders, stall (A) and watchtower (B) ----------
const wallBlocks = [];
{
  const stone = std(0x6b6460);
  for (let i = 0; i < 9; i++) { const row = i < 6 ? 0 : 1, col = row ? (i - 6) * 2 + 0.5 : i; const b = mesh(new THREE.BoxGeometry(0.55, 0.42, 0.45), i % 2 ? stone : std(0x77706a), -1.4 + col * 0.56, 0.21 + row * 0.42, 1.7); wallBlocks.push(b); }
  const shaft = std(0x5a3a1a), fl = std(0xeeeeee);
  for (let i = 0; i < 9; i++) {
    const a = new THREE.Group(); a.position.set(-1.3 + i * 0.33, 0.25 + (i * 37 % 5) * 0.12, 1.95); a.rotation.set(-0.5 - (i % 3) * 0.12, 0, (i % 2 ? 0.2 : -0.2));
    mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.5, 4), shaft, 0, 0.25, 0, a); mesh(new THREE.BoxGeometry(0.06, 0.1, 0.005), fl, 0, 0.47, 0, a); scene.add(a);
  }
}
// orcs
const orcs = [];
{
  const skin = std(0x4f7a2e, { flatShading: false }), leather = std(0x3a2414), dark = std(0x1c1612), bone = std(0xe8dcc0), wood = std(0x5a3a1a), eyeM = glow(0xff3a1a);
  const SLOTS = [[-1.6, -0.6], [1.7, -0.7], [-2.5, 0.4], [2.6, 0.3], [-1.1, 0.9], [1.2, 0.9], [-3.2, -0.8], [3.3, -0.9], [-2.0, -1.8], [2.1, -1.9], [-0.6, -2.2], [0.7, -2.3], [-3.6, 1.0], [3.7, 1.1]];
  SLOTS.forEach(([x, z], i) => {
    const o = new THREE.Group(), body = new THREE.Group(); o.add(body);
    [-1, 1].forEach(s => mesh(new THREE.CylinderGeometry(0.07, 0.06, 0.34, 6), dark, s * 0.1, 0.17, 0, body));
    mesh(new THREE.CylinderGeometry(0.2, 0.24, 0.42, 8), leather, 0, 0.55, 0, body);
    mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.06, 8), dark, 0, 0.38, 0, body);
    [-1, 1].forEach(s => { const a = mesh(new THREE.CylinderGeometry(0.06, 0.05, 0.38, 6), skin, s * 0.29, 0.56, 0, body); a.rotation.z = s * 0.25; });
    const head = mesh(new THREE.SphereGeometry(0.17, 12, 10), skin, 0, 0.9, 0.02, body); head.scale.set(1.1, 0.95, 1);
    [-1, 1].forEach(s => { const e = mesh(new THREE.ConeGeometry(0.05, 0.2, 4), skin, s * 0.2, 0.96, 0, body); e.rotation.z = -s * 1.2; mesh(new THREE.SphereGeometry(0.025, 6, 6), eyeM, s * 0.06, 0.93, 0.17, body); const tk = mesh(new THREE.ConeGeometry(0.018, 0.07, 4), bone, s * 0.06, 0.82, 0.16, body); });
    const club = new THREE.Group(); club.position.set(0.34, 0.4, 0.06); club.rotation.z = -0.3 + (i % 3) * 0.2; body.add(club);
    mesh(new THREE.CylinderGeometry(0.03, 0.05, 0.6, 6), wood, 0, 0.3, 0, club);
    if (i % 2) { mesh(new THREE.ConeGeometry(0.05, 0.16, 4), std(0x777777), 0, 0.66, 0, club); } else { mesh(new THREE.DodecahedronGeometry(0.08, 0), wood, 0, 0.6, 0, club); }
    o.userData = { slot: new THREE.Vector3(x, 0, z), start: new THREE.Vector3(x * 0.3, 0, -10 - i * 0.4), body };
    o.rotation.y = -x * 0.06; o.visible = false; scene.add(o); orcs.push(o);
  });
}
// riders on the ridge
const riders = new THREE.Group(), riderList = [];
{
  const horse = std(0x1a1414), cloth = std(0x3a3020), iron = metal(0x6a6a72), torchM = glow(0xffb02a);
  for (let i = 0; i < 7; i++) {
    const r = new THREE.Group();
    mesh(new THREE.BoxGeometry(0.45, 0.42, 1.2), horse, 0, 1.05, 0, r);
    [[-0.15, -0.45], [0.15, -0.45], [-0.15, 0.45], [0.15, 0.45]].forEach(([x, z]) => mesh(new THREE.CylinderGeometry(0.06, 0.05, 0.85, 5), horse, x, 0.42, z, r));
    const neck = mesh(new THREE.BoxGeometry(0.22, 0.6, 0.25), horse, 0, 1.45, 0.6, r); neck.rotation.x = 0.5;
    mesh(new THREE.BoxGeometry(0.2, 0.22, 0.45), horse, 0, 1.7, 0.85, r);
    mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.6, 7), cloth, 0, 1.55, -0.05, r);
    mesh(new THREE.SphereGeometry(0.13, 8, 6), iron, 0, 1.97, -0.05, r);
    mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.9, 4), iron, 0.25, 1.9, 0.1, r);
    mesh(new THREE.ConeGeometry(0.07, 0.2, 5), torchM, -0.25, 2.05, 0.05, r);
    r.userData.base = new THREE.Vector3(-9 + i * 1.3, 0, -15.5 - (i % 2) * 1.2);
    r.rotation.y = 0.15; riders.add(r); riderList.push(r);
  }
  const rl = new THREE.PointLight(0xffa040, 0, 18); rl.position.set(-5, 3, -13); riders.add(rl); riders.userData.light = rl;
  scene.add(riders);
}
// option A: stall with pigs
const stall = new THREE.Group();
{
  const wood = std(0x6b4a2a), roof = std(0x7a2a1a), pig = std(0xe8a0a0, { flatShading: false });
  for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.7, 5), wood, Math.cos(a) * 1.0, 0.35, Math.sin(a) * 0.8, stall); }
  [0.25, 0.55].forEach(y => { const ring = mesh(new THREE.TorusGeometry(0.9, 0.025, 4, 16), wood, 0, y, 0, stall); ring.rotation.x = Math.PI / 2; ring.scale.set(1.1, 0.9, 1); });
  const hut = new THREE.Group(); hut.position.set(-0.4, 0, -0.5); stall.add(hut);
  mesh(new THREE.BoxGeometry(0.8, 0.6, 0.6), wood, 0, 0.3, 0, hut);
  const rf = mesh(new THREE.ConeGeometry(0.65, 0.45, 4), roof, 0, 0.82, 0, hut); rf.rotation.y = Math.PI / 4;
  [[0.2, 0.2], [-0.2, 0.35]].forEach(([x, z], k) => { const p = new THREE.Group(); p.position.set(x + 0.2, 0, z); p.rotation.y = k ? 2 : -0.6; stall.add(p);
    const b = mesh(new THREE.SphereGeometry(0.2, 10, 8), pig, 0, 0.25, 0, p); b.scale.set(1, 0.8, 1.3);
    mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.06, 8), std(0xd07070), 0, 0.27, 0.27, p).rotation.x = Math.PI / 2;
    [[-0.08, -0.12], [0.08, -0.12], [-0.08, 0.12], [0.08, 0.12]].forEach(([lx, lz]) => mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.14, 5), pig, lx, 0.07, lz, p)); });
  stall.position.set(-3, 0, 0.4); stall.scale.setScalar(1e-4); scene.add(stall);
}
// option B: watchtower with an archer
const watch = new THREE.Group();
{
  const wood = std(0x6b4a2a), roof = std(0x7a2a1a), cloth = std(0x2a2a2a);
  [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]].forEach(([x, z]) => { const l = mesh(new THREE.CylinderGeometry(0.06, 0.08, 2.6, 6), wood, x * 0.85, 1.3, z * 0.85, watch); l.rotation.z = -x * 0.08; l.rotation.x = z * 0.08; });
  [0.8, 1.6].forEach(y => mesh(new THREE.BoxGeometry(1.0, 0.06, 0.06), wood, 0, y, 0.45, watch));
  mesh(new THREE.BoxGeometry(1.3, 0.1, 1.3), wood, 0, 2.6, 0, watch);
  for (let k = 0; k < 4; k++) { const rl = mesh(new THREE.BoxGeometry(1.3, 0.35, 0.05), wood, 0, 2.82, 0, watch); rl.rotation.y = k * Math.PI / 2; rl.position.x = Math.sin(k * Math.PI / 2) * 0.62; rl.position.z = Math.cos(k * Math.PI / 2) * 0.62; }
  const rf = mesh(new THREE.ConeGeometry(1.05, 0.8, 4), roof, 0, 3.6, 0, watch); rf.rotation.y = Math.PI / 4;
  [-1, 1].forEach(s => mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.9, 4), wood, s * 0.55, 3.15, s * 0.55, watch));
  mesh(new THREE.CylinderGeometry(0.12, 0.15, 0.45, 7), cloth, 0, 2.95, 0.2, watch);
  mesh(new THREE.SphereGeometry(0.11, 8, 6), std(0x4f7a2e), 0, 3.27, 0.2, watch);
  const bow = mesh(new THREE.TorusGeometry(0.22, 0.015, 4, 12, Math.PI), wood, 0.15, 3.0, 0.42, watch); bow.rotation.z = -Math.PI / 2;
  watch.position.set(3.2, 0, 0.5); watch.scale.setScalar(1e-4); scene.add(watch);
}
const PLATZ_GHOST = GHOSTS[0]; PLATZ_GHOST.position.set(2.0, 0, 1.0);

''')

# camera, day/night, renderAt
cut('// ---------- camera path on the master clock', '// ---------- avatar', r'''// ---------- camera path: [time, position, target] ----------
const E = EYE_WORLD;
const K = [
  [0.0, [E.x - 4.5, E.y - 4.0, E.z + 17.0], [E.x, E.y - 2.0, E.z]],
  [1.2, [E.x - 3.8, E.y - 4.4, E.z + 14.5], [E.x, E.y - 2.2, E.z]],
  [2.3, [0.8, 2.4, 8.0], [0, 1.0, 1.5]],
  [3.9, [-0.6, 2.2, 7.2], [0, 1.0, 1.5]],
  [4.3, [0.4, 1.3, 5.6], [0, 2.05, 0]],
  [5.2, [-0.2, 1.25, 5.3], [0, 2.05, 0]],
  [5.7, [-1.5, 2.6, 8.0], [-4, 2.0, -14]],
  [6.7, [-1.9, 2.8, 7.6], [-4, 2.0, -14]],
  [7.1, [0.6, 2.25, 6.6], [0, 1.95, 0]],
  [8.3, [-0.3, 2.2, 6.3], [0, 1.95, 0]],
  [8.9, [2.6, 3.0, 8.4], [0, 0.8, -1]],
  [10.0, [0.5, 6.0, 11.0], [0, 1.0, -0.5]],
  [11.2, [-2.0, 5.6, 10.4], [0, 1.0, -0.5]],
  [11.8, [3.0, 1.5, 4.8], [1.8, 0.8, -0.2]],
  [12.9, [3.4, 1.5, 4.5], [1.8, 0.8, -0.2]],
  [13.4, [0.4, 2.5, 6.6], [0, 2.3, 0]],
  [14.3, [-0.2, 2.5, 6.4], [0, 2.3, 0]],
  [14.9, [-1.5, 2.6, 8.0], [-4, 2.0, -14]],
  [16.0, [-1.9, 2.8, 7.6], [-4, 2.0, -14]],
  [16.6, [0, 4.4, 10.2], [0, 1.0, 0]],
  [18.9, [1.5, 4.8, 9.8], [0, 1.0, 0]],
  [19.4, [0.4, 2.25, 6.0], [0, 1.95, 0]],
  [21.9, [-0.6, 2.2, 5.6], [0, 1.95, 0]],
  [22.4, [-1.6, 2.3, 5.6], [-2.8, 0.8, 0.4]],
  [23.6, [-2.4, 2.2, 5.2], [-2.8, 0.8, 0.4]],
  [24.1, [2.0, 2.9, 7.0], [3.1, 1.7, 0.5]],
  [26.2, [2.6, 2.9, 6.6], [3.1, 1.7, 0.5]],
  [27.0, [0, 6.5, 15], [-2, 2.5, -6]],
  [29.1, [1.2, 7.0, 15.8], [-2, 2.5, -6]]
].map(([t, p, q]) => [t, new THREE.Vector3(...p), new THREE.Vector3(...q)]);
const _p = new THREE.Vector3(), _q = new THREE.Vector3();
function cameraAt(m, t) {
  let i = 0; while (i < K.length - 2 && m > K[i + 1][0]) i++;
  const [ta, pa, qa] = K[i], [tb, pb, qb] = K[i + 1], u = ease(ramp(m, ta, tb));
  _p.lerpVectors(pa, pb, u); _q.lerpVectors(qa, qb, u);
  _p.x += Math.sin(t * 0.7) * 0.05; _p.y += Math.sin(t * 0.9 + 1) * 0.035;
  camera.position.copy(_p); camera.lookAt(_q);
}
const C = h => new THREE.Color(h);
const DAY = { top: C(0x3a1636), bottom: C(0xf58a3a), fog: C(0x8a3a24), hemi: C(0xffc080), sun: C(0xffa860), sunI: 2.4, hemiI: 1.5 };
const NIGHT = { top: C(0x05041a), bottom: C(0x2a1640), fog: C(0x120a24), hemi: C(0x5a6aa0), sun: C(0x7080c0), sunI: 0.7, hemiI: 0.6 };
const nightAt = m => clamp(ramp(m, 14.4, 15.0) - ramp(m, 16.1, 16.7) + ramp(m, 26.3, 26.9), 0, 1);
const _v = new THREE.Vector3();
function placeAt(el, obj, yOff) { obj.getWorldPosition(_v); _v.y += yOff; _v.project(camera); el.style.left = ((_v.x + 1) / 2 * 1080).toFixed(1) + "px"; el.style.top = ((1 - _v.y) / 2 * 1920).toFixed(1) + "px"; }
const platzEl = document.getElementById("platz");

// ---------- the one function that draws time t ----------
function renderAt(t) {
  const m = unwarp(t);
  cameraAt(m, t);
  const n = nightAt(m);
  skyMat.uniforms.top.value.copy(DAY.top).lerp(NIGHT.top, n);
  skyMat.uniforms.bottom.value.copy(DAY.bottom).lerp(NIGHT.bottom, n);
  scene.fog.color.copy(DAY.fog).lerp(NIGHT.fog, n);
  hemi.color.copy(DAY.hemi).lerp(NIGHT.hemi, n); hemi.intensity = DAY.hemiI + (NIGHT.hemiI - DAY.hemiI) * n;
  sun.color.copy(DAY.sun).lerp(NIGHT.sun, n); sun.intensity = DAY.sunI + (NIGHT.sunI - DAY.sunI) * n;
  fill.intensity = 14 - 6 * n; moon.material.opacity = n;
  const pulse = 1 + 0.07 * Math.sin(t * 3.9);
  eye.scale.setScalar(pulse); eyeLight.intensity = (40 + 30 * n) * pulse;
  flames.forEach((f, i) => { const s = 1 + 0.25 * Math.sin(t * 17 + i * 2.1) + 0.1 * Math.sin(t * 29 + i); f.scale.set(1, s, 1); f.userData.light.intensity = 5 + 2 * s; });
  lavaTex.offset.x = -t * 0.08;
  smokes.forEach(s => { const k = ((t * 0.25 + s.userData.o) % 4) / 4; s.position.set(s.userData.x + k * 3, 12 + k * 14, s.userData.z); s.scale.setScalar(2 + k * 6); s.material.opacity = 0.8 * (1 - k); });

  // Sauron: triumph at "gehalten", sag at "null", shock at the riders, scroll for the vote
  const hop = bump(m, 4.5, 0.3, 0.3) + bump(m, 9.4, 0.25, 0.22) + bump(m, 15.45, 0.3, 0.3);
  sau.position.y = 0.02 * Math.sin(t * 6) + hop;
  sau.scale.y = 1 - 0.06 * bump(m, 13.75, 0.4, 1);
  const holdsPlan = live(m, 19.1, 21.95);
  sword.visible = false; mace.visible = !holdsPlan; blueprint.visible = holdsPlan;
  blueprint.scale.setScalar(holdsPlan ? Math.max(0.01, popIn(m, 19.1, 0.3)) : 1);
  sauArm.rotation.z = 1.2 * ease(clamp(ramp(m, 4.4, 4.6) - ramp(m, 5.6, 5.9), 0, 1));
  sauArm.visible = !holdsPlan;
  const shocked = live(m, 15.45, 16.1) || m >= 27.4;
  eyesShock.visible = shocked; eyesAngry.visible = !shocked;
  const cp = cape.geometry.attributes.position;
  for (let i = 0; i < cp.count; i++) { const b = i * 3, v = (0.725 - capeBase[b + 1]) / 1.45; cp.setXYZ(i, capeBase[b] + Math.sin(t * 1.7 + capeBase[b + 1] * 3) * 0.03 * v, capeBase[b + 1], capeBase[b + 2] - (0.04 + 0.03 * Math.sin(t * 2.3 + capeBase[b] * 4)) * v * v); }
  cp.needsUpdate = true;

  // new orcs march in and stay; they droop when hungry
  const shown = Math.min(NEW_ORKS, orcs.length);
  orcs.forEach((o, i) => {
    const t0 = 8.4 + i * 0.1, on = i < shown && m >= t0;
    o.visible = on; if (!on) return;
    const k = ease(ramp(m, t0, t0 + 1.0));
    o.position.lerpVectors(o.userData.start, o.userData.slot, k);
    o.position.y = k < 1 ? Math.abs(Math.sin((m - t0) * 14)) * 0.08 : 0.01 * Math.sin(t * 4 + i);
    const hungry = ramp(m, 11.4, 11.8) - ramp(m, 13.9, 14.3);
    o.userData.body.rotation.x = 0.3 * hungry; o.userData.body.rotation.z = 0.06 * hungry * Math.sin(t * 9 + i);
  });
  // a free slot among them
  PLATZ_GHOST.scale.setScalar(live(m, 17.3, 19.0) ? Math.max(1e-4, 0.5 * popIn(m, 17.3)) : 1e-4);
  GHOSTS.forEach((g, i) => { if (i) g.scale.setScalar(1e-4); });
  ghost0.scale.setScalar(1e-4);
  // elves retreat at dawn
  const elfOn = m < 6.8;
  elves.visible = elfOn; elves.userData.light.intensity = elfOn ? 12 : 0;
  elfList.forEach((e, i) => { const back = ease(ramp(m, 5.3, 6.8)); e.position.copy(e.userData.base); e.position.z -= back * 10; e.rotation.y = 0.35 + Math.PI * Math.min(1, back * 3); });
  // riders appear at night and advance at the end
  const ridOn = live(m, 14.6, 16.2) || m >= 26.4;
  riders.visible = ridOn; riders.userData.light.intensity = ridOn ? 20 : 0;
  riderList.forEach((r, i) => { const rise = m < 26 ? popIn(m, 14.6 + i * 0.06, 0.4) : 1; const adv = ease(ramp(m, 26.6, 29.1)); r.position.copy(r.userData.base); r.position.z += adv * 7; r.position.y = (rise - 1) * 2.4 + (adv > 0 ? Math.abs(Math.sin(t * 8 + i)) * 0.06 : 0); });
  // option A / B
  stall.scale.setScalar(live(m, 22.3, 26.25) ? Math.max(1e-4, popIn(m, 22.3, 0.45)) : 1e-4);
  watch.scale.setScalar(live(m, 24.1, 26.25) ? Math.max(1e-4, popIn(m, 24.1, 0.45)) : 1e-4);

  const ep = embGeo.attributes.position;
  for (let i = 0; i < EMB; i++) { const b = i * 4, y = (embBase[b + 1] + t * embBase[b + 3]) % 12; ep.setXYZ(i, embBase[b] + Math.sin(t * 0.8 + i) * 0.3, y, embBase[b + 2]); }
  ep.needsUpdate = true;
  renderer.render(scene, camera);
  placeAt(platzEl, PLATZ_GHOST, 1.2);
}

''')

# overlay timeline
cut('  // sign\n', '  // captions\n', r'''  // sign
  tl.fromTo("#signwrap", { y: -700 }, { y: 0, duration: 0.32, ease: "power4.in" }, 0);
  tl.fromTo("#signboard", { scaleY: 1 }, { scaleY: 0.9, transformOrigin: "50% 0%", duration: 0.07, yoyo: true, repeat: 1, ease: "power2.out" }, 0.32);
  tl.fromTo("#shake", { x: 0, y: 0 }, { keyframes: [{ x: -14, y: 10 }, { x: 12, y: -8 }, { x: -8, y: 6 }, { x: 5, y: -3 }, { x: 0, y: 0 }], duration: 0.35, ease: "none" }, 0.32);
  tl.fromTo("#signtitle", { filter: "drop-shadow(0 0 40px rgba(255,160,40,1)) drop-shadow(0 5px 0 #0a0708)" }, { filter: "drop-shadow(0 0 14px rgba(255,120,20,.85)) drop-shadow(0 5px 0 #0a0708)", duration: 0.8 }, 0.32);
  tl.to("#signwrap", { rotation: 1.5, transformOrigin: "50% 0%", duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0.7);
  tl.to("#signwrap", { y: -900, duration: 0.4, ease: "power3.in" }, 2.2);
  // HUD
  show("#hud", 2.9, 99);
  tl.fromTo("#hud .glowwrap", { y: -140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.08 }, 2.9);
  tl.to("#hud2", { scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }, 3.2);
  const cnt = { v: 1 }, hudOrks = document.getElementById("hudorks");
  hudOrks.textContent = "1";
  tl.fromTo(cnt, { v: 1 }, { v: 1 + NEW_ORKS, duration: 0.9, ease: "power1.inOut", onUpdate: () => { hudOrks.textContent = Math.round(cnt.v); } }, 10.0);
  tl.to("#hud1", { scale: 1.18, duration: 0.15, yoyo: true, repeat: 1 }, 10.9);
  tl.to("#hud3red", { opacity: 1, duration: 0.2 }, 13.7);
  tl.to("#hud3wrap", { scale: 1.18, duration: 0.15, yoyo: true, repeat: 1 }, 13.7);
  // the wall held
  show("#held", 3.95, 5.3); pop("#held", 3.95); out("#held", 5.1);
  // new followers
  show("#follow1", 6.9, 8.5); pop("#follow1 .fav", 6.9);
  tl.fromTo("#follow1 .fhand", { x: 80, y: 120, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }, 7.1);
  tl.to("#follow1 .fhand", { scale: 0.85, duration: 0.08, yoyo: true, repeat: 1 }, 7.4);
  tl.to("#follow1 .fcheck", { opacity: 1, duration: 0.12 }, 7.48);
  tl.fromTo("#follow1 .fplus", { scale: 1 }, { scale: 1.3, duration: 0.12, yoyo: true, repeat: 1 }, 7.48);
  out("#follow1", 8.3);
  document.getElementById("neworksnum").textContent = "+" + NEW_ORKS;
  show("#neworks", 8.6, 10.0); pop("#neworks", 8.6);
  tl.fromTo("#neworksnum", { scale: 1 }, { scale: 1.2, duration: 0.15, yoyo: true, repeat: 1 }, 9.4);
  out("#neworks", 9.8);
  // hunger
  show("#food", 13.0, 14.3); pop("#food", 13.0); out("#food", 14.1);
  // riders
  show("#night", 14.3, 16.0); pop("#night", 14.35);
  tl.fromTo("#nightred", { x: 0 }, { x: 10, duration: 0.05, yoyo: true, repeat: 9 }, 15.4);
  out("#night", 15.85);
  // follow CTA + your slot
  show("#follow2", 16.1, 17.4); pop("#follow2", 16.1);
  tl.fromTo("#follow2 .fhand", { x: 80, y: 120, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.25 }, 16.3);
  tl.to("#follow2 .ftbtn", { scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }, 16.6);
  tl.to(["#follow2 .done", "#follow2 .fcheck"], { opacity: 1, duration: 0.12 }, 16.68);
  out("#follow2", 17.25);
  show("#platz", 17.4, 19.0); pop("#platzin", 17.4); out("#platzin", 18.85);
  // top comment
  show("#comment", 20.45, 22.0);
  tl.fromTo("#ccard", { y: -500, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.6)" }, 20.45);
  tl.fromTo("#wirbauen", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 20.9);
  out("#comment", 21.8);
  // choice
  show("#choice", 22.0, 26.25);
  tl.fromTo("#cardA", { y: -900, rotation: -12 }, { y: 0, rotation: -4, duration: 0.5, ease: "back.out(1.5)" }, 22.0);
  tl.fromTo("#cardB", { y: -900, rotation: 12, opacity: 0 }, { y: 0, rotation: 4, opacity: 1, duration: 0.5, ease: "back.out(1.5)" }, 23.7);
  tl.fromTo("#oder", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }, 23.75);
  tl.to(["#cardA", "#cardB", "#oder"], { y: -900, duration: 0.3, ease: "power3.in" }, 25.95);
  // ask
  show("#ask", 26.3, 99); pop("#ask", 26.3);
  tl.fromTo("#askq", { rotation: 0 }, { rotation: 5, duration: 0.12, yoyo: true, repeat: 7, ease: "sine.inOut" }, 26.8);
''')
R('const OVERLAYS = ["#hud", "#follow1", "#count", "#ich", "#profile", "#weapons", "#night", "#follow2", "#platz", "#og", "#comment", "#choice", "#ask"];\n', '')
R('gsap.set(["#ichin", "#platzin"], { xPercent: -50, yPercent: -100 });', 'gsap.set(["#platzin"], { xPercent: -50, yPercent: -100 });')
R('  ghost0.scale.setScalar(1e-4);\n  renderer.render(scene, pc);', '  ghost0.scale.setScalar(1e-4); orcs.forEach(o => o.visible = false); stall.scale.setScalar(1e-4); watch.scale.setScalar(1e-4);\n  renderer.render(scene, pc);')
open('index.html', 'w').write(s)
print("ok", len(s))
