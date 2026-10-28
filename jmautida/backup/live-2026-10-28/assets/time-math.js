/* Integer-minute arithmetic shared by the time calculator and its tests. */
(function (root) {
  'use strict';
  function clockMinutes(value) {
    if (!/^\d{2}:\d{2}$/.test(value)) throw new Error('Enter a complete start and logout time.');
    const [h, m] = value.split(':').map(Number);
    if (h > 23 || m > 59) throw new Error('Enter a valid time.');
    return h * 60 + m;
  }
  function breakMinutes(values) {
    let total = 0;
    for (const value of values) {
      const n = Number(value);
      if (String(value).trim() === '' || !Number.isInteger(n) || n < 0 || n > 10080) throw new Error('Enter breaks in whole minutes, from 0 to 10,080.');
      total += n;
    }
    if (total > 10080) throw new Error('Total breaks cannot exceed one week (10,080 minutes).');
    return total;
  }
  function fromTarget(start, hours, breaks) {
    const startMinute = clockMinutes(start), n = Number(hours);
    if (String(hours).trim() === '' || !Number.isFinite(n) || n <= 0 || n > 168) throw new Error('Enter target hours greater than 0 and no more than 168.');
    const paid = Math.round(n * 60);
    if (paid < 1) throw new Error('Target time must round to at least one minute.');
    const unpaid = breakMinutes(breaks), elapsed = paid + unpaid, absolute = startMinute + elapsed;
    const day = Math.floor(absolute / 1440), minute = absolute % 1440;
    return {paid, unpaid, elapsed, day, minute, hours:n, rounded:Math.abs(n * 60 - paid) > 0.000001};
  }
  function fromFinish(start, finish, dayValue, breaks) {
    const startMinute = clockMinutes(start), minute = clockMinutes(finish);
    const day = dayValue === 'auto' ? (minute <= startMinute ? 1 : 0) : Number(dayValue);
    if (!Number.isInteger(day) || day < 0 || day > 14) throw new Error('Choose a logout day from the same day through 14 days later.');
    const unpaid = breakMinutes(breaks), elapsed = day * 1440 + minute - startMinute, paid = elapsed - unpaid;
    if (elapsed <= 0) throw new Error('Logout must be after your start time. Choose the next day for an overnight shift.');
    if (paid <= 0) throw new Error('Breaks must be shorter than the total shift. At least one paid minute is required.');
    if (paid > 10080) throw new Error('Paid time cannot exceed 168 hours. Check the logout day.');
    return {paid, unpaid, elapsed, day, minute, hours:Number((paid / 60).toFixed(6)), rounded:false};
  }
  const api = {clockMinutes, breakMinutes, fromTarget, fromFinish};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.JMTime = api;
})(typeof window !== 'undefined' ? window : globalThis);
