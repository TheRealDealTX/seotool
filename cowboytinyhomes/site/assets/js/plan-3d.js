// Interactive 3D model on plan pages. Loads three.js and the plan's model.json only when
// the 3D tab is opened. Drag to orbit, scroll or pinch to zoom, "Roof off" for a cutaway
// (on two-story plans it also lifts off the second floor to show the main floor).
const VIEWERS = new WeakMap();

export async function mount(el) {
  if (VIEWERS.has(el)) return VIEWERS.get(el);
  const status = el.querySelector('.viewer-status');
  try {
    const [THREE, data] = await Promise.all([
      import('/assets/js/vendor/three-0.160.0.module.min.js'),
      fetch(el.dataset.model).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }),
    ]);
    const v = build(THREE, el, data);
    VIEWERS.set(el, v);
    if (status) status.remove();
    return v;
  } catch (e) {
    if (status) status.textContent = 'The 3D model could not be loaded. Please refresh the page.';
    throw e;
  }
}

function build(THREE, el, data) {
  const canvas = el.querySelector('canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xeef4f3);
  const camera = new THREE.PerspectiveCamera(35, 1, 0.5, 2000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a9a8f, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(-40, 60, 80);
  scene.add(sun);

  // Model axes: x = width, y = depth (front at 0), z = up. three.js: y up, so map (x, z, -y)
  // and center the whole model (porches included) on the origin.
  const [bx0, by0, bx1, by1] = data.bbox || [0, 0, data.W, data.D];
  const root = new THREE.Group();
  root.rotation.x = -Math.PI / 2;
  root.position.set(-(bx0 + bx1) / 2, 0, (by0 + by1) / 2);
  scene.add(root);
  const groups = {};
  for (const [gname, mats] of Object.entries(data.groups)) {
    const g = new THREE.Group();
    for (const [mat, arr] of Object.entries(mats)) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(arr, 3));
      geo.computeVertexNormals();
      const glass = mat === 'glass';
      const m = new THREE.MeshLambertMaterial({ color: data.materials[mat] || '#cccccc', side: THREE.DoubleSide,
        transparent: glass, opacity: glass ? 0.45 : 1 });
      g.add(new THREE.Mesh(geo, m));
    }
    groups[gname] = g;
    root.add(g);
  }
  const ground = new THREE.Mesh(new THREE.CircleGeometry(Math.max(bx1 - bx0, by1 - by0) * 1.6, 48),
    new THREE.MeshLambertMaterial({ color: 0xd7e2d2 }));
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  scene.add(ground);

  // Orbit state
  const size = Math.max(bx1 - bx0, by1 - by0, data.H);
  const st = { theta: -0.75, phi: 1.12, r: Math.max(size * 1.6, data.H * 3.2), target: new THREE.Vector3(0, data.H * 0.35, 0) };
  const home = { ...st, target: st.target.clone() };
  function place() {
    st.phi = Math.max(0.15, Math.min(1.52, st.phi));
    st.r = Math.max(size * 0.6, Math.min(size * 5, st.r));
    camera.position.set(
      st.target.x + st.r * Math.sin(st.phi) * Math.sin(st.theta),
      st.target.y + st.r * Math.cos(st.phi),
      st.target.z + st.r * Math.sin(st.phi) * Math.cos(st.theta));
    camera.lookAt(st.target);
    render();
  }
  function resize() {
    const w = el.clientWidth, h = +el.dataset.height || Math.round(Math.min(560, Math.max(300, w * 0.6)));
    renderer.setSize(w, h, false);
    canvas.style.height = h + 'px';
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    render();
  }
  function render() { renderer.render(scene, camera); }

  let drag = null;
  const pts = new Map();
  canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); drag = [e.clientX, e.clientY]; });
  canvas.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId)) return;
    const prev = pts.get(e.pointerId);
    pts.set(e.pointerId, [e.clientX, e.clientY]);
    if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      const other = [...pts.entries()].find(([id]) => id !== e.pointerId)[1];
      const before = Math.hypot(prev[0] - other[0], prev[1] - other[1]);
      const now = Math.hypot(a[0] - b[0], a[1] - b[1]);
      if (before > 0) st.r *= before / now;
    } else {
      st.theta -= (e.clientX - prev[0]) * 0.008;
      st.phi -= (e.clientY - prev[1]) * 0.008;
    }
    place();
  });
  const up = e => { pts.delete(e.pointerId); drag = null; };
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('pointercancel', up);
  canvas.addEventListener('wheel', e => { e.preventDefault(); st.r *= Math.exp(e.deltaY * 0.0012); place(); }, { passive: false });

  el.querySelectorAll('[data-3d]').forEach(btn => btn.addEventListener('click', () => {
    const a = btn.dataset['3d'];
    if (a === 'roof') {
      const on = !groups.roof.visible;
      setRoof(on);
      btn.setAttribute('aria-pressed', String(!on));
      btn.textContent = on ? 'Roof off (see inside)' : 'Roof on';
    } else if (a === 'reset') {
      Object.assign(st, { ...home, target: home.target.clone() });
    } else if (a === 'top') {
      Object.assign(st, { theta: 0, phi: 0.16, r: size * 2.2 });
      if (groups.roof.visible) el.querySelector('[data-3d="roof"]').click();
    } else if (a === 'front') {
      Object.assign(st, { theta: 0, phi: 1.35, r: size * 2.1 });
    }
    place();
  }));
  function setRoof(on) {
    groups.roof.visible = on;
    if (groups.upper) groups.upper.visible = on;
  }
  new ResizeObserver(resize).observe(el);
  resize();
  place();
  return {
    render, renderer,
    // Used by the build to render stills: view({ theta, phi, zoom }), roof(false) for a cutaway.
    view(o) { Object.assign(st, { theta: o.theta ?? st.theta, phi: o.phi ?? st.phi, r: Math.max(size, data.H * 2) * (o.zoom ?? 1.6) }); place(); },
    roof(on) { setRoof(on); render(); },
  };
}
