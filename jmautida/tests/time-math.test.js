// Run: node jmautida/tests/time-math.test.js
const assert = require('assert');
const T = require('../public/assets/js/time-math.js');

const r1 = T.fromTarget('19:30', '9.3', []);
assert.deepStrictEqual([r1.day, r1.minute, r1.paid], [1, 4 * 60 + 48, 558]);
const r2 = T.fromTarget('19:30', '9.3', ['30']);
assert.deepStrictEqual([r2.day, r2.minute], [1, 5 * 60 + 18]);
const r3 = T.fromFinish('19:30', '05:18', 'auto', ['30', '30']);
assert.strictEqual(r3.hours, 8.8);
assert.throws(() => T.fromFinish('09:00', '09:00', '0', []), /after your start/);
assert.throws(() => T.breakMinutes(['1.5']), /whole minutes/);

assert.strictEqual(T.shiftMinutes('09:00', '17:30', '30'), 480);
assert.strictEqual(T.shiftMinutes('22:00', '06:00', ''), 480);
assert.strictEqual(T.shiftMinutes('', '', ''), 0);
assert.throws(() => T.shiftMinutes('09:00', '', '0'), /both/);
assert.throws(() => T.shiftMinutes('09:00', '09:30', '45'), /longer/);

const w = T.weekTotals([600, 600, 600, 600, 600], 40, 20, 1.5);
assert.deepStrictEqual(w, { total: 3000, regular: 2400, overtime: 600, pay: 1100 });
assert.strictEqual(T.weekTotals([120], 40, '', 1.5).pay, 0);

assert.deepStrictEqual(T.decimalToClock('7.75'), { h: 7, m: 45, minutes: 465 });
assert.deepStrictEqual(T.decimalToClock('0.3'), { h: 0, m: 18, minutes: 18 });
assert.throws(() => T.decimalToClock('-1'));
console.log('time-math: all tests passed');
