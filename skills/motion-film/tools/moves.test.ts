// bun moves.test.ts — fails loudly if a move's endpoints break
import * as M from "./moves";
const near = (a: number, b: number, e = 1e-3) => { if (Math.abs(a - b) > e) throw new Error(`${a} != ${b}`); };
near(M.spring(0), 0); near(M.spring(3), 1); if (M.spring(0.15, 0.4, 16) <= 1) throw new Error("underdamped spring must overshoot");
near(M.wordRise(5, 0).y, 0); near(M.wordRise(5, 0).s, 1);
const z = M.zoomThrough(2, 0, 1, { x: 100, y: 100, w: 480, h: 270 }); near(z.s, 4); near(z.tx + 340 * z.s, 960); near(z.ty + 235 * z.s, 540);
near(M.zoomThrough(0, 0, 1, { x: 0, y: 0, w: 480, h: 270 }).s, 1);
const r = M.morphRect(9, 0, 1, { x: 0, y: 0, w: 10, h: 10 }, { x: 50, y: 60, w: 200, h: 100, r: 24 }); near(r.x, 50); near(r.r, 24);
near(M.iris(1, 0, 1, 960, 540).r, Math.hypot(960, 540));
near(M.impact(-1, 0).sx, 1); near(M.shake(0.5, [1]).x, 0);
near(M.camera(10, [{ t: 0, x: 0, y: 0, zoom: 1 }, { t: 1, x: 100, y: 0, zoom: 4 }]).zoom, 4);
near(M.camera(0.5, [{ t: 0, x: 0, y: 0, zoom: 1 }, { t: 1, x: 100, y: 0, zoom: 4 }]).zoom, 2);
if (M.typeOn(10, 0, "hello").str !== "hello") throw new Error("typeOn");
if (M.staccato(1.5, [[0, "A"], [1, "B"], [2, "C"]]).word !== "B") throw new Error("staccato");
console.log("moves ok");
