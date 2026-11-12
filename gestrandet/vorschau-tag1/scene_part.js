<script type="importmap">{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js", "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/" } }</script>
<script type="module">
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { Water } from "three/addons/objects/Water.js";
import { Sky } from "three/addons/objects/Sky.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

const W = __EVENTS__;
const CAPS = __CAPS__;
const DUR = W.dur;

// ---------- helpers ----------
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const ease = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const ramp = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const bump = (t, t0, d, h) => (t > t0 && t < t0 + d) ? h * Math.sin(Math.PI * (t - t0) / d) : 0;
const live = (t, a, b) => t >= a && t < b;
const smooth = (a, b, x) => { const u = clamp((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); };
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let r = Math.imul(seed ^ seed >>> 15, 1 | seed); r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r; return ((r ^ r >>> 14) >>> 0) / 4294967296; }; }
const R = rng(23);
// value noise + fbm (deterministic)
function hash(x, y) { let h = x * 374761393 + y * 668265263; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0) / 4294967296; }
function vnoise(x, y) { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1); return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v; }
function fbm(x, y) { let s = 0, a = 0.5, f = 1; for (let i = 0; i < 5; i++) { s += a * vnoise(x * f, y * f); f *= 2.03; a *= 0.5; } return s; }

// ---------- the island: one height function ----------
const VOLC = new THREE.Vector2(-28, -38);
function heightAt(x, z) {
  const ang = Math.atan2(z, x), r = Math.hypot(x, z * 1.12);
  const coast = 135 + 22 * (fbm(Math.cos(ang) * 2 + 7, Math.sin(ang) * 2 + 3) - 0.5) * 2 + 10 * Math.sin(ang * 3 + 1);
  const land = smooth(coast + 6, coast - 26, r);
  const hills = 3 + 14 * fbm(x * 0.018 + 11, z * 0.018 + 5) + 8 * Math.pow(fbm(x * 0.04, z * 0.04), 2);
  const dv = Math.hypot(x - VOLC.x, z - VOLC.y);
  const volc = 62 * Math.exp(-(dv * dv) / (2 * 30 * 30)) - 14 * Math.exp(-(dv * dv) / (2 * 5 * 5));
  return -4 + land * (4.6 + hills * smooth(0, 30, coast - r) + volc);
}

// ---------- renderer / scene ----------
const canvas = document.getElementById("gl");
let renderer;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" }); }
catch (e) { const f = document.getElementById("fail"); f.textContent = "Dein Gerät kann die 3D-Vorschau nicht anzeigen (WebGL fehlt). Bitte am PC oder in einem anderen Browser öffnen."; f.style.display = "flex"; throw e; }
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.55;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0xbfd8e8, 0.0016);
const camera = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.05, 6000);
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.85, ...o });
const mesh = (geo, mat, x = 0, y = 0, z = 0, parent = scene) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); parent.add(m); return m; };
function canvasTex(w, h, draw) { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }

// sky + sun
const sky = new Sky(); sky.scale.setScalar(4500); scene.add(sky);
const su = sky.material.uniforms; su.turbidity.value = 3; su.rayleigh.value = 1.4; su.mieCoefficient.value = 0.004; su.mieDirectionalG.value = 0.82;
const sunDir = new THREE.Vector3().setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - 24), THREE.MathUtils.degToRad(200));
su.sunPosition.value.copy(sunDir);
const stormDome = new THREE.Mesh(new THREE.SphereGeometry(4000, 32, 16), new THREE.MeshBasicMaterial({ color: 0x1c222b, side: THREE.BackSide, transparent: true, opacity: 0, fog: false, depthWrite: false }));
scene.add(stormDome);
const hemi = new THREE.HemisphereLight(0xcfe8ff, 0xb8955a, 1.2); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0d8, 3.2); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.04;
const sc = sun.shadow.camera; sc.left = -22; sc.right = 22; sc.top = 22; sc.bottom = -22; sc.near = 1; sc.far = 260;
scene.add(sun); scene.add(sun.target);

// terrain
const TS = 420, TN = 300;
const terrainGeo = new THREE.PlaneGeometry(TS, TS, TN, TN); terrainGeo.rotateX(-Math.PI / 2);
{
  const p = terrainGeo.attributes.position, col = new Float32Array(p.count * 3), c = new THREE.Color();
  const SAND = new THREE.Color(0xe6cf94), WET = new THREE.Color(0xbfa46a), GRASS = new THREE.Color(0x4f9a3a), JUNGLE = new THREE.Color(0x2f7a2c), ROCK = new THREE.Color(0x7a7066), ASH = new THREE.Color(0x4a4440), SEA = new THREE.Color(0x3fc6c0);
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), h = heightAt(x, z); p.setY(i, h); }
  terrainGeo.computeVertexNormals();
  const n = terrainGeo.attributes.normal;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), z = p.getZ(i), h = p.getY(i), slope = 1 - n.getY(i), nz = fbm(x * 0.08, z * 0.08);
    if (h < -0.4) c.copy(SEA).lerp(WET, smooth(-3.5, -0.4, h));
    else if (h < 0.5) c.copy(WET).lerp(SAND, smooth(-0.4, 0.5, h));
    else if (h < 2.2 + nz * 1.5) c.copy(SAND);
    else if (h < 3.4 + nz * 1.5) c.copy(SAND).lerp(GRASS, smooth(2.2, 3.4, h - nz * 1.5));
    else c.copy(GRASS).lerp(JUNGLE, smooth(0.35, 0.75, nz));
    if (slope > 0.32 || h > 34) c.lerp(ROCK, smooth(0.3, 0.5, slope) * 0.9 + smooth(30, 40, h) * 0.6);
    if (h > 44) c.lerp(ASH, smooth(44, 56, h));
    col.set([c.r, c.g, c.b], i * 3);
  }
  terrainGeo.setAttribute("color", new THREE.BufferAttribute(col, 3));
}
const terrain = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, flatShading: false }));
terrain.receiveShadow = true; scene.add(terrain);
// volcano glow + smoke
const crater = mesh(new THREE.CircleGeometry(4.5, 24), new THREE.MeshBasicMaterial({ color: 0xff6a1a }), VOLC.x, heightAt(VOLC.x, VOLC.y) + 0.6, VOLC.y); crater.rotation.x = -Math.PI / 2;
const smokeTex = canvasTex(128, 128, (c, w, h) => { const g = c.createRadialGradient(64, 64, 4, 64, 64, 64); g.addColorStop(0, "rgba(90,85,85,0.7)"); g.addColorStop(1, "rgba(90,85,85,0)"); c.fillStyle = g; c.fillRect(0, 0, w, h); });
const smokes = []; for (let i = 0; i < 16; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: smokeTex, depthWrite: false, transparent: true })); s.userData.o = i / 16 * 6; scene.add(s); smokes.push(s); }

// water
const waterNormals = new THREE.TextureLoader().load("assets/waternormals.jpg", t => { t.wrapS = t.wrapT = THREE.RepeatWrapping; });
const water = new Water(new THREE.PlaneGeometry(6000, 6000), { textureWidth: 512, textureHeight: 512, waterNormals, sunDirection: sunDir.clone(), sunColor: 0xffffff, waterColor: 0x0b6f86, distortionScale: 2.6, fog: true, alpha: 0.92 });
water.rotation.x = -Math.PI / 2; water.position.y = 0.05; water.material.transparent = true; scene.add(water);

// ---------- vegetation (instanced) ----------
function palmGeometries() {
  const pts = []; for (let i = 0; i <= 10; i++) { const u = i / 10; pts.push(new THREE.Vector3(1.2 * u * u, 6.2 * u, 0)); }
  const curve = new THREE.CatmullRomCurve3(pts);
  const trunk = new THREE.TubeGeometry(curve, 16, 0.2, 8, false);
  { const p = trunk.attributes.position; for (let i = 0; i < p.count; i++) { const y = p.getY(i), k = 1 - 0.45 * (y / 6.2); const ring = 1 + 0.08 * Math.max(0, Math.sin(y * 9)); p.setX(i, (p.getX(i) - 1.2 * Math.pow(y / 6.2, 2)) * k * ring + 1.2 * Math.pow(y / 6.2, 2)); p.setZ(i, p.getZ(i) * k * ring); } trunk.computeVertexNormals(); }
  const top = new THREE.Vector3(1.2, 6.2, 0), leaves = [];
  for (let k = 0; k < 9; k++) {
    const L = 3.2, g = new THREE.PlaneGeometry(L, 0.9, 10, 2); g.translate(L / 2, 0, 0);
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), u = x / L; p.setY(i, y * (1 - u * 0.85) * Math.sin(Math.PI * Math.min(1, u * 1.4 + 0.15))); p.setZ(i, -1.6 * u * u + Math.abs(y) * 0.25); }
    g.rotateX(Math.PI / 2); g.rotateZ(0.25); g.rotateY(k / 9 * Math.PI * 2 + (k % 2) * 0.2); g.translate(top.x, top.y, top.z); g.computeVertexNormals(); leaves.push(g);
  }
  const coco = []; for (let k = 0; k < 4; k++) { const s = new THREE.SphereGeometry(0.17, 8, 6); s.translate(top.x + Math.cos(k * 1.6) * 0.22, top.y - 0.25, Math.sin(k * 1.6) * 0.22); coco.push(s); }
  return { trunk, leaves: mergeGeometries(leaves), coco: mergeGeometries(coco) };
}
const PG = palmGeometries();
const veg = { palms: [], bushes: [], rocks: [], ferns: [] };
let GUY_POS;
{
  // hero beach: walk down the +z axis until we hit dry sand
  let z = 175; while (z > 0 && heightAt(3, z) < 0.55) z -= 0.25; GUY_POS = new THREE.Vector3(3, heightAt(3, z - 2.2), z - 2.2);
  const R2 = rng(91);
  for (let i = 0; i < 9000 && veg.palms.length < 700; i++) {
    const x = (R2() - 0.5) * 360, zz = (R2() - 0.5) * 360, h = heightAt(x, zz);
    if (h < 1.4 || h > 30) continue;
    if (Math.hypot(x - GUY_POS.x, zz - GUY_POS.z) < 7) continue;
    const beachy = h < 7, dens = beachy ? 0.55 : 0.18;
    if (R2() > dens) continue;
    veg.palms.push([x, h - 0.2, zz, R2() * 6.28, 0.75 + R2() * 0.55]);
  }
  for (let i = 0; i < 14000 && veg.bushes.length < 1600; i++) {
    const x = (R2() - 0.5) * 360, zz = (R2() - 0.5) * 360, h = heightAt(x, zz);
    if (h < 3 || h > 38) continue; if (Math.hypot(x - GUY_POS.x, zz - GUY_POS.z) < 6) continue;
    veg.bushes.push([x, h, zz, R2() * 6.28, 0.8 + R2() * 1.8]);
  }
  for (let i = 0; i < 4000 && veg.rocks.length < 300; i++) {
    const x = (R2() - 0.5) * 360, zz = (R2() - 0.5) * 360, h = heightAt(x, zz);
    if (h < -1 || h > 60) continue; if (R2() > (h > 25 ? 0.9 : 0.25)) continue; if (Math.hypot(x - GUY_POS.x, zz - GUY_POS.z) < 4) continue;
    veg.rocks.push([x, h, zz, R2() * 6.28, 0.3 + R2() * (h > 25 ? 3 : 1.2)]);
  }
  // a few palms framing the hero
  [[-6, -3, 1.0], [5.5, -4.5, 1.1], [-9, -7, 0.9], [8.5, -9, 1.0], [-3, -10, 1.15]].forEach(([dx, dz, s]) => { const x = GUY_POS.x + dx, zz = GUY_POS.z + dz; veg.palms.push([x, heightAt(x, zz) - 0.2, zz, R2() * 6.28, s]); });
}
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _s = new THREE.Vector3(), _pp = new THREE.Vector3(), _e = new THREE.Euler();
function instanced(geo, mat, list, tilt = 0, shadow = true) {
  const im = new THREE.InstancedMesh(geo, mat, list.length);
  list.forEach(([x, y, z, r, s], i) => { _e.set((R() - 0.5) * tilt, r, (R() - 0.5) * tilt); _q.setFromEuler(_e); _s.set(s, s, s); _pp.set(x, y, z); _m.compose(_pp, _q, _s); im.setMatrixAt(i, _m); });
  im.castShadow = shadow; im.receiveShadow = true; scene.add(im); return im;
}
const trunkMat = std(0x9a7448, { roughness: 0.95 });
const leafMat = new THREE.MeshStandardMaterial({ color: 0x3f9a3a, roughness: 0.7, side: THREE.DoubleSide });
const palmTrunks = instanced(PG.trunk, trunkMat, veg.palms, 0.25);
const palmLeaves = instanced(PG.leaves, leafMat, veg.palms, 0.25);
instanced(PG.coco, std(0x5a3a1a), veg.palms, 0.25, false);
const bushGeo = (() => { const g = new THREE.IcosahedronGeometry(1, 1); const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const v = new THREE.Vector3().fromBufferAttribute(p, i); v.multiplyScalar(0.85 + 0.3 * hash(Math.round(v.x * 10), Math.round(v.z * 10 + v.y * 7))); v.y *= 0.7; p.setXYZ(i, v.x, v.y + 0.3, v.z); } g.computeVertexNormals(); return g; })();
instanced(bushGeo, std(0x2f8a34, { roughness: 0.8 }), veg.bushes, 0.3);
const rockGeo = new THREE.DodecahedronGeometry(1, 1); { const p = rockGeo.attributes.position; for (let i = 0; i < p.count; i++) { p.setY(i, p.getY(i) * 0.6); } rockGeo.computeVertexNormals(); }
instanced(rockGeo, std(0x8a8278, { roughness: 1, flatShading: true }), veg.rocks, 0.6);

// wreck + debris + paddle
{
  const g = new THREE.Group(); g.position.set(GUY_POS.x + 9, -0.4, GUY_POS.z + 16); g.rotation.set(0.3, -0.7, 0.45); scene.add(g);
  const hullPts = []; for (let i = 0; i <= 10; i++) { const u = i / 10; hullPts.push(new THREE.Vector2(0.15 + 1.1 * Math.sin(u * Math.PI * 0.5), -0.6 + u * 1.2)); }
  const hull = mesh(new THREE.LatheGeometry(hullPts, 18, 0, Math.PI), std(0xa0703e, { side: THREE.DoubleSide }), 0, 0, 0, g); hull.rotation.z = Math.PI / 2; hull.scale.set(1, 2.4, 1);
  const mast = mesh(new THREE.CylinderGeometry(0.06, 0.07, 2.6, 8), std(0x6a4a2a), 0.4, 1.3, 0, g); mast.rotation.z = 0.8; mast.castShadow = true;
  const sail = mesh(new THREE.PlaneGeometry(1.4, 1.1), std(0xeae4d4, { side: THREE.DoubleSide }), 1.0, 1.7, 0.2, g); sail.rotation.set(0.3, 0.4, 0.7);
  for (let i = 0; i < 9; i++) { const p = mesh(new THREE.BoxGeometry(1 + R() * 0.8, 0.08, 0.22), std(0xa8743f), GUY_POS.x - 6 + R() * 16, 0.05, GUY_POS.z + 5 + R() * 10); p.rotation.y = R() * 3; }
  const pd = new THREE.Group(); pd.position.set(GUY_POS.x - 1.6, GUY_POS.y, GUY_POS.z - 0.6); pd.rotation.z = 0.25; scene.add(pd);
  mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.6, 8), std(0x8a5a32), 0, 0.6, 0, pd).castShadow = true;
  const bl = mesh(new THREE.SphereGeometry(0.22, 12, 10), std(0xc98a4a), 0, 1.5, 0, pd); bl.scale.set(0.8, 1.6, 0.25); bl.castShadow = true;
}
// Kevin the coconut
const kevin = new THREE.Group();
{
  const faceTex = canvasTex(256, 128, (c, w, h) => { c.fillStyle = "#6e4220"; c.fillRect(0, 0, w, h); for (let i = 0; i < 260; i++) { c.fillStyle = `rgba(40,20,8,${0.2 + (i % 5) * 0.06})`; c.fillRect((i * 37) % w, (i * 53) % h, 6, 2); } c.fillStyle = "#fff"; c.beginPath(); c.arc(112, 54, 11, 0, 7); c.arc(146, 54, 11, 0, 7); c.fill(); c.fillStyle = "#111"; c.beginPath(); c.arc(114, 56, 5, 0, 7); c.arc(148, 56, 5, 0, 7); c.fill(); c.strokeStyle = "#fff"; c.lineWidth = 5; c.lineCap = "round"; c.beginPath(); c.arc(129, 72, 18, 0.2, Math.PI - 0.2); c.stroke(); c.lineWidth = 4; c.beginPath(); c.moveTo(98, 38); c.lineTo(120, 34); c.moveTo(138, 34); c.lineTo(160, 38); c.stroke(); });
  faceTex.offset.x = 0.25;
  const k = mesh(new THREE.SphereGeometry(0.17, 24, 16), new THREE.MeshStandardMaterial({ map: faceTex, roughness: 0.85 }), 0, 0, 0, kevin); k.rotation.y = -Math.PI / 2; k.castShadow = true;
  scene.add(kevin);
}
let KEVIN_GROUND;

// clouds
const cloudTex = canvasTex(256, 128, (c, w, h) => { for (let i = 0; i < 7; i++) { const g = c.createRadialGradient(40 + i * 30, 70 + Math.sin(i) * 12, 4, 40 + i * 30, 70 + Math.sin(i) * 12, 50); g.addColorStop(0, "rgba(255,255,255,0.95)"); g.addColorStop(1, "rgba(255,255,255,0)"); c.fillStyle = g; c.fillRect(0, 0, w, h); } });
const clouds = [];
for (let i = 0; i < 26; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: cloudTex, transparent: true, depthWrite: false, fog: false })); const storm = i >= 14; s.userData = { a: R() * 6.28, d: storm ? 380 + R() * 120 : 600 + R() * 500, y: storm ? 60 + R() * 40 : 120 + R() * 90, sc: storm ? 160 + R() * 120 : 140 + R() * 160, storm }; scene.add(s); clouds.push(s); }

// splash, rain, lightning
const SPL = 90, splash = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.1, 0), new THREE.MeshBasicMaterial({ color: 0xffffff }), SPL); splash.frustumCulled = false; scene.add(splash);
const splData = Array.from({ length: SPL }, () => ({ vx: (R() - 0.5) * 4, vy: 3 + R() * 4, vz: (R() - 0.2) * 3, s: 0.6 + R() * 1.4 }));
const RAIN = 1400, rainGeo = new THREE.BufferGeometry(), rainBase = new Float32Array(RAIN * 3);
for (let i = 0; i < RAIN; i++) rainBase.set([(R() - 0.5) * 40, R() * 25, (R() - 0.5) * 40], i * 3);
rainGeo.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(RAIN * 3), 3));
const rain = new THREE.Points(rainGeo, new THREE.PointsMaterial({ color: 0xcfe0ff, size: 0.06, transparent: true, opacity: 0 })); scene.add(rain);
const bolt = new THREE.Group(); scene.add(bolt); bolt.visible = false;

// ---------- characters (loaded) ----------
let guy, mixer, actions = {}, handR, parrots = [];
const loader = new GLTFLoader();
const loaded = Promise.all([
  loader.loadAsync("assets/barbarian.glb"),
  loader.loadAsync("assets/parrot.glb")
]).then(([g, p]) => {
  guy = g.scene;
  ["Barbarian_Hat", "Barbarian_Cape", "1H_Axe_Offhand", "Barbarian_Round_Shield", "1H_Axe", "2H_Axe", "Mug"].forEach(n => { const o = guy.getObjectByName(n); if (o) o.visible = false; });
  guy.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  const box = new THREE.Box3().setFromObject(guy), hgt = box.max.y - box.min.y;
  guy.scale.setScalar(1.85 / hgt);
  guy.position.copy(GUY_POS); scene.add(guy);
  handR = guy.getObjectByName("handslot.r") || guy.getObjectByName("hand.r") || guy.getObjectByName("handr");
  mixer = new THREE.AnimationMixer(guy);
  g.animations.forEach(c => { const a = mixer.clipAction(c); a.play(); a.setEffectiveWeight(0); a.paused = true; actions[c.name] = a; });
  for (let i = 0; i < 3; i++) {
    const b = p.scene.clone(); b.scale.setScalar(0.022 + i * 0.002); scene.add(b);
    const mx = new THREE.AnimationMixer(b); const a = mx.clipAction(p.animations[0]); a.play();
    parrots.push({ b, mx, ph: i * 2.1, r: 7 + i * 2.5, h: 6 + i * 1.4 });
  }
  KEVIN_GROUND = new THREE.Vector3(GUY_POS.x + 0.75, GUY_POS.y + 0.17, GUY_POS.z + 0.35);
});

// pose the character on the shared clock: [clip, start, loops?]
const SEQ = [
  ["Lie_Idle", -10, true],
  ["Lie_StandUp", W.okay - 0.35, false],
  ["Unarmed_Idle", W.okay + 1.6, true],
  ["PickUp", W.kokos - 0.7, false],
  ["Unarmed_Idle", W.kokos + 0.5, true],
  ["Hit_A", W.sturm - 0.1, false],
  ["Unarmed_Idle", W.sturm + 0.6, true],
  ["Cheer", W.du - 0.1, false],
  ["Unarmed_Idle", W.du + 1.6, true]
];
const FADE = 0.25;
function poseAt(t) {
  if (!mixer) return;
  Object.values(actions).forEach(a => a.setEffectiveWeight(0));
  let i = 0; while (i < SEQ.length - 1 && t >= SEQ[i + 1][1]) i++;
  const set = (k, w) => { const [name, st, loop] = SEQ[k], a = actions[name]; if (!a) return; const d = a.getClip().duration; let lt = t - st; lt = loop ? ((lt % d) + d) % d : clamp(lt, 0, d - 0.001); a.time = lt; a.setEffectiveWeight(a.getEffectiveWeight() + w); };
  const f = i > 0 ? ramp(t, SEQ[i][1], SEQ[i][1] + FADE) : 1;
  set(i, f); if (f < 1) set(i - 1, 1 - f);
  mixer.update(0);
}

// ---------- camera path ----------
let K;
function buildCamera() {
  const G = GUY_POS, Y = G.y, H = Y + 1.45, V = new THREE.Vector3(VOLC.x, heightAt(VOLC.x, VOLC.y), VOLC.y);
  K = [
    [0.0, [G.x + 3.2, Y + 1.8, G.z - 0.6], [G.x, Y + 0.3, G.z - 0.4]],
    [W.okay - 0.2, [G.x + 2.9, Y + 1.6, G.z - 0.2], [G.x, Y + 0.4, G.z - 0.2]],
    [W.okay + 1.4, [G.x + 1.0, H + 0.2, G.z + 3.4], [G.x, H, G.z]],
    [W.das, [G.x + 0.6, H + 0.15, G.z + 3.0], [G.x, H, G.z]],
    [W.tag - 0.2, [G.x + 70, 170, G.z + 230], [0, 10, 0]],
    [W.auf, [G.x - 40, 175, G.z + 215], [0, 10, 0]],
    [W.auf + 0.01, [-150, 70, 80], [V.x, V.y * 0.7, V.z]],
    [W.mein - 0.01, [-60, 66, 20], [V.x, V.y * 0.8, V.z]],
    [W.mein, [G.x + 0.7, H + 0.15, G.z + 3.3], [G.x + 0.15, H - 0.05, G.z]],
    [W.regel - 0.01, [G.x - 0.2, H + 0.1, G.z + 2.9], [G.x + 0.15, H - 0.05, G.z]],
    [W.regel, [G.x + 4.5, Y + 3.2, G.z + 8.5], [G.x, Y + 1.2, G.z]],
    [W.aktuell - 0.01, [G.x + 3.5, Y + 2.8, G.z + 7.5], [G.x, Y + 1.2, G.z]],
    [W.aktuell, [G.x - 1.3, H + 0.1, G.z + 3.6], [G.x + 0.4, H - 0.3, G.z]],
    [W.und - 0.01, [G.x - 1.0, H + 0.05, G.z + 3.3], [G.x + 0.4, H - 0.3, G.z]],
    [W.und, [G.x - 0.3, Y + 2.9, G.z - 4.6], [G.x - 0.3, Y + 3.5, G.z + 40]],
    [W.huette - 0.01, [G.x - 0.2, Y + 3.0, G.z - 4.0], [G.x - 0.2, Y + 4.5, G.z + 40]],
    [W.huette, [G.x + 3, Y + 11, G.z + 18], [G.x, Y + 1, G.z - 6]],
    [W.du - 0.01, [G.x + 5, Y + 11.5, G.z + 17], [G.x, Y + 1, G.z - 6]],
    [W.du, [G.x + 1.2, H + 0.2, G.z + 3.8], [G.x + 0.3, H - 0.1, G.z]],
    [DUR, [G.x + 0.9, H + 0.15, G.z + 3.1], [G.x + 0.3, H - 0.1, G.z]]
  ].map(([t, p, q]) => [t, new THREE.Vector3(...p), new THREE.Vector3(...q)]);
}
const _cp = new THREE.Vector3(), _cq = new THREE.Vector3();
function cameraAt(t) {
  let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const [ta, pa, qa] = K[i], [tb, pb, qb] = K[i + 1], u = tb - ta < 0.02 ? 1 : ease(ramp(t, ta, tb));
  _cp.lerpVectors(pa, pb, u); _cq.lerpVectors(qa, qb, u);
  _cp.x += Math.sin(t * 0.8) * 0.04; _cp.y += Math.sin(t * 1.1 + 1) * 0.03;
  camera.position.copy(_cp); camera.lookAt(_cq);
}
const stormAt = t => ramp(t, W.und, W.sturm + 0.3) * 0.85 - ramp(t, W.huette, W.huette + 0.6) * 0.4;
const FOG_DAY = new THREE.Color(0xbfd8e8), FOG_STORM = new THREE.Color(0x2e3640);
const _v = new THREE.Vector3();
function placeAt(el, obj, yOff) { obj.getWorldPosition(_v); _v.y += yOff; _v.project(camera); el.style.left = ((_v.x + 1) / 2 * 1080).toFixed(1) + "px"; el.style.top = ((1 - _v.y) / 2 * 1920).toFixed(1) + "px"; }
const kevTagEl = document.getElementById("kevtag");

// post-processing
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(540, 960), 0.28, 0.5, 0.88); composer.addPass(bloom);
composer.addPass(new OutputPass());

// ---------- the one function that draws time t ----------
function renderAt(t) {
  if (!guy) return;
  cameraAt(t);
  const s = stormAt(t);
  stormDome.material.opacity = 0.88 * s; scene.fog.color.copy(FOG_DAY).lerp(FOG_STORM, s); scene.fog.density = 0.0016 + 0.004 * s;
  hemi.intensity = 1.2 - 0.8 * s; sun.intensity = 3.2 * (1 - 0.85 * s); renderer.toneMappingExposure = 0.55 + 0.25 * s;
  water.material.uniforms.time.value = t * 0.7; water.material.uniforms.distortionScale.value = 2.6 + 5 * s;
  water.material.uniforms.waterColor.value.setHex(s > 0.3 ? 0x0a3a48 : 0x0b6f86);
  clouds.forEach(c => { const u = c.userData, a = u.a + t * 0.004 * (1 + 5 * s); c.position.set(GUY_POS.x + Math.cos(a) * u.d, u.y, GUY_POS.z + Math.sin(a) * u.d + (u.storm ? 380 - s * 200 : 0)); c.scale.set(u.sc, u.sc * 0.45, 1); c.material.color.setScalar(1 - 0.75 * s); c.material.opacity = u.storm ? s : 1; });
  smokes.forEach(sp => { const k = ((t * 0.12 + sp.userData.o) % 6) / 6; sp.position.set(VOLC.x + k * 18, heightAt(VOLC.x, VOLC.y) + 2 + k * 40, VOLC.y - k * 6); sp.scale.setScalar(8 + k * 30); sp.material.opacity = 0.75 * (1 - k); });
  palmLeaves.rotation.y = 0;
  // shadow camera follows the hero
  sun.position.copy(GUY_POS).addScaledVector(sunDir, 120); sun.target.position.copy(GUY_POS);
  // character
  poseAt(t);
  guy.position.set(GUY_POS.x, GUY_POS.y, GUY_POS.z); guy.rotation.y = 0;
  // Kevin in hand from "Kokosnuss" to "Regel" and from "Du entscheidest" on
  const holding = live(t, W.kokos - 0.1, W.regel) || t >= W.du + 0.9;
  if (holding && handR) { handR.updateWorldMatrix(true, false); handR.getWorldPosition(kevin.position); kevin.position.y += 0.05; }
  else kevin.position.copy(KEVIN_GROUND);
  kevin.rotation.y = t > W.kevinEnd ? -0.7 * ease(ramp(t, W.kevinEnd, W.kevinEnd + 0.3)) : Math.sin(t * 2) * 0.1;
  // parrots circle the beach
  parrots.forEach(p => { const a = t * 0.7 + p.ph; p.b.position.set(GUY_POS.x + Math.cos(a) * p.r, GUY_POS.y + p.h + Math.sin(t * 1.3 + p.ph) * 0.8, GUY_POS.z - 2 + Math.sin(a) * p.r); p.b.rotation.y = -a; p.mx.setTime(t + p.ph); p.b.visible = s < 0.3; });
  // splash
  for (let i = 0; i < SPL; i++) { const d = splData[i], a = t - 0.05; let k = 0; _pp.set(0, -50, 0);
    if (a > 0 && a < 1.1) { _pp.set(GUY_POS.x - 0.8 + d.vx * a, GUY_POS.y + d.vy * a - 6 * a * a, GUY_POS.z + 2.5 + d.vz * a * 0.5); k = 0.6 * d.s * (1 - a / 1.1); }
    _m.compose(_pp, _q.identity(), _s.set(k, k, k)); splash.setMatrixAt(i, _m); }
  splash.instanceMatrix.needsUpdate = true;
  rain.material.opacity = 0.8 * ramp(t, W.und + 0.4, W.sturm) * (1 - ramp(t, W.huette, W.huette + 0.5) * 0.6);
  const rp = rainGeo.attributes.position;
  for (let i = 0; i < RAIN; i++) { const b = i * 3; rp.setXYZ(i, rainBase[b] + GUY_POS.x - t * 2, GUY_POS.y + ((rainBase[b + 1] - t * 22) % 25 + 25) % 25, rainBase[b + 2] + GUY_POS.z + 6); }
  rp.needsUpdate = true;
  bolt.visible = live(t, W.sturm - 0.05, W.sturm + 0.12) || live(t, W.sturm + 0.25, W.sturm + 0.32);
  composer.render();
  placeAt(kevTagEl, kevin, 0.3);
}
function buildBolt() {
  const pts = []; let x = GUY_POS.x - 30, y = 160; for (let i = 0; i < 14; i++) { pts.push(new THREE.Vector3(x, y, GUY_POS.z + 260)); x += (R() - 0.5) * 18; y -= 12; }
  bolt.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xffffff, fog: false })));
}

// ---------- treasure map drawn from the real terrain ----------
function drawMap() {
  const c = document.getElementById("mapcv"), g = c.getContext("2d"), N = c.width, img = g.createImageData(N, N);
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const x = (i / N - 0.5) * 340, z = (j / N - 0.5) * 340, h = heightAt(x, z), k = (j * N + i) * 4;
    let r = 214, gg = 190, b = 140;
    if (h < 0) { const d = clamp(-h / 4, 0, 1); r = 150 - 40 * d; gg = 170 - 30 * d; b = 150 - 10 * d; }
    else if (h < 2.5) { r = 222; gg = 196; b = 140; }
    else if (h < 40) { r = 150 - h; gg = 160 - h * 0.6; b = 100 - h; }
    else { r = 120; gg = 105; b = 90; }
    if (h > 0 && Math.abs(h % 8) < 0.5) { r -= 30; gg -= 30; b -= 30; }
    img.data[k] = r; img.data[k + 1] = gg; img.data[k + 2] = b; img.data[k + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  // fog of war: only a small patch around the hero is explored
  const gx = (GUY_POS.x / 340 + 0.5) * N, gz = (GUY_POS.z / 340 + 0.5) * N;
  g.save(); g.globalCompositeOperation = "source-over";
  const fog = g.createRadialGradient(gx, gz, N * 0.05, gx, gz, N * 0.13);
  fog.addColorStop(0, "rgba(70,55,40,0)"); fog.addColorStop(1, "rgba(70,55,40,0.86)");
  g.fillStyle = fog; g.fillRect(0, 0, N, N); g.restore();
  g.strokeStyle = "#b01818"; g.lineWidth = N * 0.012; g.lineCap = "round";
  g.beginPath(); g.moveTo(gx - N * 0.025, gz - N * 0.025); g.lineTo(gx + N * 0.025, gz + N * 0.025); g.moveTo(gx + N * 0.025, gz - N * 0.025); g.lineTo(gx - N * 0.025, gz + N * 0.025); g.stroke();
  g.fillStyle = "#3a2410"; g.font = `${Math.round(N * 0.05)}px "Lilita One", sans-serif`; g.textAlign = "center";
  [["VULKAN?", VOLC.x, VOLC.y - 22], ["DSCHUNGEL?", 45, -10], ["HÖHLE?", 70, 60], ["???", -80, 55]].forEach(([s, x, z]) => g.fillText(s, (x / 340 + 0.5) * N, (z / 340 + 0.5) * N));
}

// ---------- avatar ----------
function makeAvatar() {
  poseAt(W.okay + 3); guy.position.copy(GUY_POS);
  const head = new THREE.Vector3(GUY_POS.x, GUY_POS.y + 1.45, GUY_POS.z);
  const pc = new THREE.PerspectiveCamera(30, 1, 0.05, 6000);
  pc.position.set(head.x + 0.4, head.y + 0.1, head.z + 2.2); pc.lookAt(head.x, head.y - 0.05, head.z);
  renderer.setPixelRatio(1); renderer.setSize(512, 512, false);
  renderer.render(scene, pc);
  document.getElementById("avatar").src = canvas.toDataURL("image/jpeg", 0.9);
}
