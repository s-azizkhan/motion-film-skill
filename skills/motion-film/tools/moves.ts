// Move library for raea films. Every move is a pure function of absolute time T (seconds) → numbers to apply as styles.
// Copy into the project (`cp $MT/moves.ts film/video/`) and import from "./moves".
// Families: enter (something arrives) · carry (next beat grows out of this one) · contact (one thing causes another) · camera.

export const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const seg = (T: number, t0: number, t1: number) => clamp((T - t0) / (t1 - t0));
export const smooth = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const expoOut = (x: number) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp(x)));
export const expoInOut = (x: number) => { x = clamp(x); return x === 0 ? 0 : x === 1 ? 1 : x < 0.5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2; };
export const sineInOut = (x: number) => -(Math.cos(Math.PI * clamp(x)) - 1) / 2;
export const backOut = (x: number, k = 1.7) => { x = clamp(x) - 1; return 1 + (k + 1) * x * x * x + k * x * x; };
export const rng = (seed: number) => () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };

// Damped spring step response 0→1 at time `tau` after start. zeta < 1 overshoots.
export function spring(tau: number, zeta = 0.55, omega = 16): number {
  if (tau <= 0) return 0;
  if (zeta >= 1) return 1 - (1 + omega * tau) * Math.exp(-omega * tau);
  const wd = omega * Math.sqrt(1 - zeta * zeta);
  return 1 - Math.exp(-zeta * omega * tau) * (Math.cos(wd * tau) + ((zeta * omega) / wd) * Math.sin(wd * tau));
}
// SwiftUI-style: duration d, bounce b (0 smooth, .15 snappy, .3 bouncy).
export const swift = (tau: number, d = 0.5, b = 0.15) => spring(tau, 1 - b, (2 * Math.PI) / d);

// ── enter ────────────────────────────────────────────────────────────────────────────────────────────────────
// A word lands: spring rise + scale; opacity leads so it never reads as a fade.
export function wordRise(T: number, t0: number, { dist = 60, s0 = 0.86, zeta = 0.6, omega = 15 } = {}) {
  const p = spring(T - t0, zeta, omega);
  return { op: clamp((T - t0) / 0.08), y: (1 - p) * dist, s: lerp(s0, 1, p) };
}
// Letters of a wordmark drop one by one; speed squashes them, the spring restores.
export function letterDrop(T: number, t0: number, i: number, { stagger = 0.045, dist = 220, squash = 0.35 } = {}) {
  const tau = T - t0 - i * stagger, p = spring(tau, 0.42, 18), v = Math.abs(spring(tau + 0.01, 0.42, 18) - p) * 100;
  const sq = clamp(v * squash * 0.1, 0, squash);
  return { op: tau > 0 ? 1 : 0, y: -(1 - p) * dist, sx: 1 + sq * 0.6, sy: 1 - sq };
}
export function popIn(T: number, t0: number, { rise = 30, s0 = 0.6 } = {}) {
  const p = spring(T - t0, 0.5, 17);
  return { op: clamp((T - t0) / 0.06), s: lerp(s0, 1, p), dy: (1 - p) * rise };
}
export function liftOut(T: number, t1: number, { dur = 0.35, dist = 40 } = {}) {
  const p = expoOut(seg(T, t1, t1 + dur));
  return { op: 1 - p, dy: -dist * p, s: 1 + 0.06 * p };
}
// Lines rise from behind a clip (wrap each line in overflow:hidden).
export function maskRise(T: number, t0: number, i: number, { stagger = 0.08, dist = 1 } = {}) {
  const p = expoOut(seg(T, t0 + i * stagger, t0 + i * stagger + 0.55));
  return { y: (1 - p) * dist * 100 /* % of line height */, visible: T >= t0 + i * stagger };
}
export function typeOn(T: number, t0: number, text: string, { cps = 22, blink = 0.53 } = {}) {
  const n = clamp(Math.floor((T - t0) * cps), 0, text.length), done = n >= text.length;
  return { n, str: text.slice(0, n), done, caret: !done || Math.floor((T - t0) / blink) % 2 === 0 };
}
export function counter(T: number, t0: number, t1: number, from: number, to: number) {
  return lerp(from, to, expoOut(seg(T, t0, t1)));
}

// ── carry ────────────────────────────────────────────────────────────────────────────────────────────────────
export type Rect = { x: number; y: number; w: number; h: number; r?: number };
// One rect becomes another (button → window, card → page). Apply to ONE element so the eye sees it change.
export function morphRect(T: number, t0: number, t1: number, A: Rect, B: Rect, ease = expoInOut): Required<Rect> & { cx: number; cy: number } {
  const p = ease(seg(T, t0, t1)), x = lerp(A.x, B.x, p), y = lerp(A.y, B.y, p), w = lerp(A.w, B.w, p), h = lerp(A.h, B.h, p);
  return { x, y, w, h, r: lerp(A.r ?? 0, B.r ?? 0, p), cx: x + w / 2, cy: y + h / 2 };
}
// A circle opens from a point until it covers a W×H frame: clipPath `circle(${r}px at ${cx}px ${cy}px)`.
export function iris(T: number, t0: number, t1: number, cx: number, cy: number, W = 1920, H = 1080) {
  const R = Math.hypot(Math.max(cx, W - cx), Math.max(cy, H - cy)), p = expoInOut(seg(T, t0, t1));
  return { r: R * p, covered: p >= 1 };
}
// Log-space push until `target` fills the frame. transformOrigin "0 0" (raea honours it): `translate(tx,ty) scale(s)`.
export function zoomThrough(T: number, t0: number, t1: number, target: Rect, W = 1920, H = 1080, fit = 1) {
  const p = expoInOut(seg(T, t0, t1)), S = fit * Math.min(W / target.w, H / target.h), s = Math.exp(lerp(0, Math.log(S), p));
  const cx = target.x + target.w / 2, cy = target.y + target.h / 2; // target's screen point slides to centre while scale grows
  return { s, tx: lerp(cx, W / 2, p) - cx * s, ty: lerp(cy, H / 2, p) - cy * s };
}
// Arc from one slot to the next; land it with impact() at t1.
export function hop(T: number, t0: number, t1: number, from: [number, number], to: [number, number], height = 160) {
  const p = sineInOut(seg(T, t0, t1));
  return { x: lerp(from[0], to[0], p), y: lerp(from[1], to[1], p) - Math.sin(Math.PI * p) * height };
}
// Many → one group on fanned arcs.
export function gather(T: number, t0: number, t1: number, i: number, n: number, from: [number, number], to: [number, number], { stagger = 0.04, arc = 120 } = {}) {
  const a = t0 + i * stagger, p = expoInOut(seg(T, a, t1 + i * stagger)), side = (i / Math.max(1, n - 1) - 0.5) * 2;
  return { x: lerp(from[0], to[0], p) + Math.sin(Math.PI * p) * arc * side, y: lerp(from[1], to[1], p), rot: (1 - p) * side * 12 };
}
// Hard-cut words: the one place a bare cut is right. list = [[t, word], ...]
export function staccato(T: number, list: [number, string][]) {
  let i = -1; for (let k = 0; k < list.length; k++) if (T >= list[k][0]) i = k;
  return { i, word: i >= 0 ? list[i][1] : "" };
}

// ── contact ──────────────────────────────────────────────────────────────────────────────────────────────────
// The landing: squash on the hit, ring out.
export function impact(T: number, tHit: number, { amt = 0.18, decay = 9, omega = 30 } = {}) {
  const tau = T - tHit; if (tau < 0) return { sx: 1, sy: 1, r: 0 };
  const r = Math.exp(-decay * tau) * Math.cos(omega * tau) * amt;
  return { sx: 1 + r, sy: 1 - r, r };
}
// A click: dip, ring, state flips at tc.
export function press(T: number, tc: number, { depth = 0.08 } = {}) {
  const tau = T - tc, down = tau > -0.08 && tau < 0 ? (tau + 0.08) / 0.08 : 0;
  const ring = tau >= 0 ? Math.exp(-10 * tau) * Math.cos(28 * tau) : 0;
  return { s: 1 - depth * (down + ring), active: tau >= 0 };
}
// Pointer along knots [{t,x,y}], shrinking on each click time.
export function cursor(T: number, knots: { t: number; x: number; y: number }[], clicks: number[] = []) {
  let k = 0; while (k < knots.length - 2 && T > knots[k + 1].t) k++;
  const A = knots[k], B = knots[Math.min(k + 1, knots.length - 1)], p = expoInOut(seg(T, A.t, B.t));
  const c = clicks.reduce((m, tc) => Math.max(m, Math.exp(-Math.pow((T - tc) / 0.06, 2))), 0);
  return { x: lerp(A.x, B.x, p), y: lerp(A.y, B.y, p), s: 1 - 0.18 * c };
}
// Stretch along velocity: rotate(ang) scale(sx, sy) rotate(-ang).
export function squash(vx: number, vy: number, { k = 0.0006, max = 0.35 } = {}) {
  const v = Math.hypot(vx, vy), e = Math.min(max, v * k);
  return { ang: (Math.atan2(vy, vx) * 180) / Math.PI, sx: 1 + e, sy: 1 / (1 + e) };
}

// ── camera ───────────────────────────────────────────────────────────────────────────────────────────────────
// Keyed camera; zoom interpolates in log space. Key the subject ~0.1 s ahead on sineInOut to follow it,
// key the landing before a snap on expoInOut to whip. Apply: translate(W/2,H/2) scale(zoom) rotate(rot) translate(-x,-y).
export type CamKey = { t: number; x: number; y: number; zoom?: number; rot?: number; ease?: (x: number) => number };
export function camera(T: number, keys: CamKey[]) {
  let k = 0; while (k < keys.length - 2 && T > keys[k + 1].t) k++;
  const A = keys[k], B = keys[Math.min(k + 1, keys.length - 1)], p = (B.ease ?? sineInOut)(A === B ? 1 : seg(T, A.t, B.t));
  return { x: lerp(A.x, B.x, p), y: lerp(A.y, B.y, p), zoom: Math.exp(lerp(Math.log(A.zoom ?? 1), Math.log(B.zoom ?? 1), p)), rot: lerp(A.rot ?? 0, B.rot ?? 0, p) };
}
export function camTransform(c: { x: number; y: number; zoom: number; rot: number }, W = 1920, H = 1080, depth = 0) {
  const z = Math.pow(c.zoom, 1 / (1 + depth)), f = 1 / (1 + depth);
  return `translate(${W / 2}px,${H / 2}px) scale(${z}) rotate(${c.rot}deg) translate(${-c.x * f}px,${-c.y * f}px)`;
}
// Deterministic shake after every landing, zero before.
export function shake(T: number, hits: number[], { amp = 14, decay = 7, freq = 23 } = {}) {
  let x = 0, y = 0, rot = 0;
  for (const h of hits) { const tau = T - h; if (tau < 0 || tau > 1) continue; const e = amp * Math.exp(-decay * tau);
    x += e * Math.sin(freq * tau * 6.28 + h); y += e * Math.cos(freq * 1.3 * tau * 6.28 + h * 2); rot += e * 0.05 * Math.sin(freq * 0.7 * tau * 6.28); }
  return { x, y, rot };
}
// Hand-held float, faded to zero inside holds [[t0,t1],...].
export function handheld(T: number, holds: [number, number][] = [], amp = 6) {
  const still = holds.some(([a, b]) => T > a && T < b) ? 0 : 1;
  return { x: still * amp * Math.sin(T * 0.9 + 1.3) * Math.sin(T * 0.37), y: still * amp * 0.7 * Math.sin(T * 0.71 + 0.4) };
}
// Slow push for a hold: 1 → 1+amount. Keep it OFF true rests (the checker counts it as motion).
export const drift = (T: number, t0: number, t1: number, amount = 0.04) => 1 + amount * sineInOut(seg(T, t0, t1));
// Whip pan: offset 0→dist with a sharp middle; pair with a swoosh SFX at t0 and the shutter render.
export const whip = (T: number, t0: number, dur: number, dist: number) => dist * expoInOut(seg(T, t0, t0 + dur));
