s = open('index.html').read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)
def cut(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]

# ---- riders: a charging cavalry plus their leader ----
cut('// riders on the ridge', '// option A: stall with pigs', r'''// the cavalry charge: riders come from the plain (+z) towards the camp; one leader breaks through
const riders = new THREE.Group(), riderList = [];
const LEADER_STOP = 8.4, LEADER_ARRIVE = 14.4;
{
  const horse = std(0x1a1414), cloth = std(0x3a3020), iron = metal(0x6a6a72), torchM = glow(0xffb02a);
  const build = (leader) => {
    const r = new THREE.Group(), b = new THREE.Group(); r.add(b);
    const hm = leader ? std(0x0c0a0a) : horse;
    mesh(new THREE.BoxGeometry(0.45, 0.42, 1.2), hm, 0, 1.05, 0, b);
    const legs = [[-0.15, -0.45], [0.15, -0.45], [-0.15, 0.45], [0.15, 0.45]].map(([x, z]) => { const g = new THREE.Group(); g.position.set(x, 0.85, z); b.add(g); mesh(new THREE.CylinderGeometry(0.06, 0.05, 0.85, 5), hm, 0, -0.42, 0, g); return g; });
    const neck = mesh(new THREE.BoxGeometry(0.22, 0.6, 0.25), hm, 0, 1.45, 0.6, b); neck.rotation.x = 0.5;
    mesh(new THREE.BoxGeometry(0.2, 0.22, 0.45), hm, 0, 1.7, 0.85, b);
    mesh(new THREE.CylinderGeometry(0.16, 0.2, 0.6, 7), leader ? std(0x5a0a0a) : cloth, 0, 1.55, -0.05, b);
    mesh(new THREE.SphereGeometry(0.13, 8, 6), iron, 0, 1.97, -0.05, b);
    mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.9, 4), iron, 0.25, 1.9, 0.1, b);
    mesh(new THREE.ConeGeometry(0.07, 0.2, 5), torchM, -0.25, 2.05, 0.05, b);
    if (leader) {
      [-1, 1].forEach(s2 => mesh(new THREE.SphereGeometry(0.03, 6, 6), glow(0xff3a1a), s2 * 0.05, 1.99, 0.07, b));
      const cp2 = mesh(new THREE.CylinderGeometry(0.2, 0.42, 0.9, 10, 1, true, Math.PI * 0.6, Math.PI * 0.8), std(0x8a1010, { side: THREE.DoubleSide }), 0, 1.4, -0.15, b);
      [-1, 1].forEach(s2 => { const h2 = mesh(new THREE.ConeGeometry(0.03, 0.22, 5), std(0xe8dcc0), s2 * 0.1, 2.12, -0.05, b); h2.rotation.z = -s2 * 0.5; });
      r.scale.setScalar(1.45);
    }
    r.userData = { body: b, legs };
    r.rotation.y = Math.PI; riders.add(r); return r;
  };
  for (let i = 0; i < 22; i++) {
    const r = build(false), row = i % 3, col = Math.floor(i / 3);
    r.userData.x0 = (col - 3.2) * 1.55 + (row % 2) * 0.7; r.userData.z0 = 36 + row * 2.2 + (i % 2) * 0.6; r.userData.fall = 9.3 + i * 0.1; r.userData.side = i % 2 ? 1 : -1;
    riderList.push(r);
  }
  const L = build(true); L.userData.x0 = 0.6; L.userData.z0 = 38; L.userData.leader = true; riderList.push(L);
  scene.add(riders);
}
const SPEED = 2.4;
function riderZ(r, t) { if (r.userData.leader) return r.userData.z0 + (LEADER_STOP - r.userData.z0) * ease(clamp(t / LEADER_ARRIVE, 0, 1)) * 0 + Math.max(LEADER_STOP, r.userData.z0 - (r.userData.z0 - LEADER_STOP) * clamp(t / LEADER_ARRIVE, 0, 1)) - r.userData.z0; return r.userData.z0 - SPEED * Math.min(t, r.userData.fall); }
const _rp = new THREE.Vector3();
function riderPos(r, t, out) { return out.set(CAMP.x + r.userData.x0, 0, CAMP.z + riderZ(r, t)); }
// arrows: four volleys from the watchtower
const ARROWS = 160, arrowMesh = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.018, 0.018, 0.9, 4), std(0x3a2414), ARROWS);
arrowMesh.frustumCulled = false; scene.add(arrowMesh);
const arrowData = [];
for (let k = 0; k < ARROWS; k++) { const w = Math.floor(k / 40); arrowData.push({ t0: 8.33 + w * 0.32 + (k % 40) * 0.01, j: (k * 7) % 22, ox: (R() - 0.5) * 1.6, oz: (R() - 0.5) * 2.0, sx: (R() - 0.5) * 1.2 }); }
// dragon fire: glowing puffs from the mouth
const FIRE = 110, fireMesh = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.35, 1), new THREE.MeshBasicMaterial({ color: 0xff7a1a, transparent: true, opacity: 0.85, fog: false, depthWrite: false }), FIRE);
fireMesh.frustumCulled = false; scene.add(fireMesh);
const fireCore = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.2, 1), new THREE.MeshBasicMaterial({ color: 0xffe08a, fog: false }), FIRE);
fireCore.frustumCulled = false; scene.add(fireCore);
const fireLight = new THREE.PointLight(0xff7a1a, 0, 22); fireLight.userData.keep = true; scene.add(fireLight);
''')

# ---- horde present from the start, cheering at the end ----
R("  const on = horde.n > 0 && m >= 8.4;", "  const on = horde.n > 0;")
R("  const hungry = ramp(m, 11.4, 11.8) - ramp(m, 13.9, 14.3);\n  horde.slots", "  const hungry = 0, cheer = m > 19.0 ? 1 : 0;\n  horde.slots")
R("const row = Math.floor(i / 22), t0 = 8.6 + row * 0.12, k = ease(ramp(m, t0, t0 + 1.3));", "const row = Math.floor(i / 22), k = 1;")
R("bob = k < 1 ? Math.abs(Math.sin((m - t0) * 12 + ph)) * 0.06 : 0.01 * Math.sin(t * 4 + ph);", "bob = 0.01 * Math.sin(t * 4 + ph) + cheer * Math.abs(Math.sin(t * 7 + ph)) * 0.35;")

# ---- watchtower always built ----
R("watch.position.set(CAMP.x + 7.5, 0, CAMP.z + 5.5); watch.scale.setScalar(1e-4); scene.add(watch);", "watch.position.set(CAMP.x + 7.5, 0, CAMP.z + 5.5); watch.scale.setScalar(1.25); scene.add(watch);")

# ---- camera path (voice time) ----
cut("const K = [", "].map(([t, p, q]) => [t, new THREE.Vector3(...p), new THREE.Vector3(...q)]);", '''const WT = [CAMP.x + 7.5, 0, CAMP.z + 5.5];
const K = [
  [0.0, CP(-1.2, 1.1, 27), CP(0.4, 1.9, 40)],
  [1.549, CP(-0.8, 1.2, 25.5), CP(0.4, 1.9, 36)],
  [1.55, CP(-9, 8.5, 2), CP(0, 0.5, 28)],
  [4.3, CP(-8, 8, 3.5), CP(0, 0.5, 24)],
  [4.31, CP(3.2, 2.2, 17.5), [WT[0], 3.6, WT[2]]],
  [7.3, CP(4.2, 2.6, 15.5), [WT[0], 3.9, WT[2]]],
  [7.31, CP(5.6, 5.0, 9.6), [WT[0], 4.0, WT[2]]],
  [8.3, CP(6.0, 5.1, 9.0), [WT[0], 4.0, WT[2]]],
  [8.31, CP(10, 7.5, 6), CP(0, 0.6, 22)],
  [9.2, CP(9, 7.8, 7), CP(0, 0.6, 20)],
  [9.21, CP(-5, 1.6, 29), CP(0.5, 1.0, 19)],
  [11.6, CP(4, 1.8, 28), CP(0, 1.0, 17)],
  [11.61, CP(1.3, 3.5, 1.6), CP(0, 2.0, 14)],
  [13.2, CP(1.1, 3.4, 2.2), CP(0, 2.0, 11)],
  [13.21, ...SC(0.3, 6.2)],
  [14.7, ...SC(-0.3, 5.6)],
  [16.6, ...SC(0.3, 5.2)],
  [16.61, CP(-4, 3.2, 17), CP(0, 3, 8)],
  [17.7, CP(-5, 3.4, 17.5), CP(0, 3, 8)],
  [17.71, CP(-9.5, 4.4, 16.5), CP(-1, 2.2, 8.5)],
  [19.5, CP(-10, 4.8, 16), CP(-1, 2.2, 8.5)],
  [19.51, ...SC(-0.4, 5.6)],
  [20.1, ...SC(0.3, 5.4)],
  [20.11, CP(0, 7, 20), CP(0, 1.2, -3)],
  [25.73, CP(1.4, 9.5, 23), CP(0, 1, -5)]
''')
R("const nightAt = m => clamp(ramp(m, 14.4, 15.0) - ramp(m, 16.1, 16.7) + ramp(m, 26.3, 26.9), 0, 1);", "const nightAt = m => 0.7;")
R("const platzEl = document.getElementById(\"platz\");\n", "")

# ---- renderAt: replace the scene logic ----
cut("  // Sauron: triumph at", "  const ep = embGeo.attributes.position;", r'''  // Sauron on his rock: raises the mace at "Feuer!", shocked when the leader breaks through, laughs at the blast
  const hop = bump(m, 8.33, 0.3, 0.25) + bump(m, 18.9, 0.35, 0.35);
  sau.position.set(PODIUM.x, PODIUM.y + 0.02 * Math.sin(t * 6) + hop, PODIUM.z); sauShadow.position.set(PODIUM.x, PODIUM.y + 0.04, PODIUM.z); fill.position.set(PODIUM.x + 0.5, PODIUM.y + 2.6, PODIUM.z + 3.2);
  sau.scale.y = 1; sau.rotation.y = 0; sau.rotation.z = live(m, 18.3, 20.0) ? 0.06 * Math.sin(t * 22) : 0;
  sword.visible = false; blueprint.visible = false; mace.visible = true; sauArm.visible = true;
  sauArm.rotation.z = 1.25 * ease(clamp(ramp(m, 8.2, 8.4) - ramp(m, 9.6, 9.9), 0, 1)) + 1.1 * ease(clamp(ramp(m, 18.8, 19.0) - ramp(m, 20.0, 20.3), 0, 1));
  const shocked = live(m, 12.6, 14.8);
  eyesShock.visible = shocked; eyesAngry.visible = !shocked;
  const cp = cape.geometry.attributes.position;
  for (let i = 0; i < cp.count; i++) { const b = i * 3, v = (0.725 - capeBase[b + 1]) / 1.45; cp.setXYZ(i, capeBase[b] + Math.sin(t * 1.7 + capeBase[b + 1] * 3) * 0.03 * v, capeBase[b + 1], capeBase[b + 2] - (0.04 + 0.03 * Math.sin(t * 2.3 + capeBase[b] * 4)) * v * v); }
  cp.needsUpdate = true;

  // the army stands in the camp; the right hand (dragon) arrives from the sky
  const rhIdx = RECRUITS.findIndex(r2 => r2[0] === RIGHT_HAND), dragonO = orcs[rhIdx];
  orcs.forEach((o, i) => {
    if (o === dragonO) return;
    o.visible = true; o.position.copy(o.userData.slot);
    if (o.userData.dragon) { o.userData.wings.forEach((wg, s2) => { wg.rotation.z = (s2 ? -1 : 1) * (0.25 + 0.2 * Math.sin(t * 2.5)); }); o.position.y = 0.04 * Math.sin(t * 2); return; }
    o.position.y = m > 19.0 ? Math.abs(Math.sin(t * 8 + i)) * 0.3 : 0.01 * Math.sin(t * 4 + i);
    o.userData.body.rotation.x = 0; o.userData.body.rotation.z = 0;
  });
  hordeAt(m, t);
  PLATZ_GHOST.scale.setScalar(1e-4); GHOSTS.forEach(g => g.scale.setScalar(1e-4)); ghost0.scale.setScalar(1e-4);
  elves.visible = false; stall.scale.setScalar(1e-4);

  // riders charge, fall one by one; the leader rides up to Sauron and burns
  let alive = 0;
  const L = riderList[riderList.length - 1];
  riderList.forEach((r, i) => {
    riderPos(r, m, _rp); r.position.copy(_rp);
    const ud = r.userData, gallop = ud.leader ? (m < LEADER_ARRIVE ? 1 : 0) : (m < ud.fall ? 1 : 0);
    ud.legs.forEach((lg, k) => { lg.rotation.x = gallop * 0.7 * Math.sin(t * 14 + k * 1.6 + i); });
    ud.body.position.y = gallop * Math.abs(Math.sin(t * 14 + i)) * 0.08;
    let fallK = 0;
    if (ud.leader) { fallK = ease(ramp(m, 18.65, 19.2)); const rear = bump(m, LEADER_ARRIVE - 0.1, 1.0, 1); ud.body.rotation.x = -0.6 * rear; }
    else fallK = ease(ramp(m, ud.fall, ud.fall + 0.45));
    ud.body.rotation.z = (ud.side || 1) * 1.45 * fallK; ud.body.position.y -= 0.35 * fallK;
    if (fallK < 0.5) alive++;
  });
  document.getElementById("hudreiter").textContent = alive;
  L.userData.body.traverse(o2 => { if (o2.isMesh && o2.material && o2.material.color && !o2.userData.c0) o2.userData.c0 = o2.material.color.getHex(); });
  const burnt = m >= 18.6;
  L.userData.body.traverse(o2 => { if (o2.isMesh && o2.userData.c0 !== undefined && !(o2.material.isMeshBasicMaterial)) o2.material.color.setHex(burnt ? 0x120a08 : o2.userData.c0); });

  // arrows
  arrowData.forEach((a, k) => {
    const life = m - a.t0, dur = 0.85;
    if (life < 0 || life > dur) { _hm.makeScale(0, 0, 0); arrowMesh.setMatrixAt(k, _hm); return; }
    const u = life / dur, tgt = riderList[a.j]; riderPos(tgt, a.t0 + dur, _rp);
    const A = new THREE.Vector3(watch.position.x + a.sx, 4.4, watch.position.z), B = new THREE.Vector3(_rp.x + a.ox, 1.2, _rp.z + a.oz);
    const P = A.clone().lerp(B, u); P.y += 6 * u * (1 - u);
    const D = B.clone().sub(A); D.y += 6 * (1 - 2 * u); D.normalize();
    _hq.setFromUnitVectors(new THREE.Vector3(0, 1, 0), D); _hs.set(1, 1, 1); _hm.compose(P, _hq, _hs); arrowMesh.setMatrixAt(k, _hm);
  });
  arrowMesh.instanceMatrix.needsUpdate = true;

  // dragon: dives in, hovers, breathes fire on the leader, then climbs away
  const LP = riderPos(L, m, new THREE.Vector3());
  if (dragonO) {
    dragonO.visible = m >= 15.6;
    const P0 = new THREE.Vector3(CAMP.x - 26, 22, CAMP.z - 24), P1 = new THREE.Vector3(LP.x - 6.5, 5.5, LP.z - 1.5), P2 = new THREE.Vector3(CAMP.x - 9, 9, CAMP.z - 8);
    const dk = ease(ramp(m, 15.6, 17.6)), up = ease(ramp(m, 19.6, 21.5));
    dragonO.position.copy(P0).lerp(P1, dk).lerp(P2, up); dragonO.position.y += 0.25 * Math.sin(t * 3);
    dragonO.lookAt(m < 19.6 ? new THREE.Vector3(LP.x, 1.2, LP.z) : new THREE.Vector3(CAMP.x, 2, CAMP.z + 20));
    dragonO.userData.wings.forEach((wg, s2) => { wg.rotation.z = (s2 ? -1 : 1) * (0.3 + 0.75 * Math.sin(t * (live(m, 17.6, 19.6) ? 5 : 9))); });
  }
  // fire
  const mouth = dragonO ? dragonO.localToWorld(new THREE.Vector3(0, 3.0, 2.5)) : new THREE.Vector3();
  const fdir = new THREE.Vector3(LP.x, 1.0, LP.z).sub(mouth); const fdist = fdir.length(); fdir.normalize();
  let fireOn = 0;
  for (let j = 0; j < FIRE; j++) {
    const te = 17.8 + j * (1.6 / FIRE), age = m - te, lifeF = 0.55;
    if (age < 0 || age > lifeF) { _hm.makeScale(0, 0, 0); fireMesh.setMatrixAt(j, _hm); fireCore.setMatrixAt(j, _hm); continue; }
    fireOn = 1; const u = age / lifeF;
    const P = mouth.clone().addScaledVector(fdir, fdist * u); P.x += Math.sin(j * 12.9) * 0.6 * u; P.y += Math.cos(j * 7.3) * 0.5 * u;
    const sc = 0.4 + 2.2 * u; _hq.identity(); _hs.set(sc, sc, sc); _hm.compose(P, _hq, _hs); fireMesh.setMatrixAt(j, _hm);
    _hs.set(sc * 0.6, sc * 0.6, sc * 0.6); _hm.compose(P, _hq, _hs); fireCore.setMatrixAt(j, _hm);
  }
  fireMesh.instanceMatrix.needsUpdate = true; fireCore.instanceMatrix.needsUpdate = true;
  fireLight.position.set(LP.x, 2.5, LP.z + 1); fireLight.intensity = fireOn ? 60 : (live(m, 18.6, 19.4) ? 40 * (1 - ramp(m, 18.6, 19.4)) : 0);

  // follow the dragon on its dive
  if (dragonO && live(m, 15.9, 17.7)) { camera.position.set(CAMP.x - 3 + Math.sin(t * 0.7) * 0.05, 3.2, CAMP.z + 17); camera.lookAt(dragonO.position.x, dragonO.position.y + 2, dragonO.position.z); }
  const RW = null, inRH = false;

''')
R("  renderer.render(scene, camera);\n  placeAt(platzEl, PLATZ_GHOST, 1.2);\n", "  renderer.render(scene, camera);\n")
open('index.html', 'w').write(s); print('stage2 ok')
