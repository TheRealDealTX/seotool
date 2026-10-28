'use strict';
document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
const search = document.querySelector('#tool-search');
if (search) {
  let category = 'All tools';
  const filter = () => {
    let count = 0;
    document.querySelectorAll('.tool-card').forEach(card => {
      const show = (category === 'All tools' || card.dataset.category === category) && card.dataset.search.includes(search.value.trim().toLowerCase());
      card.hidden = !show;
      if (show) count++;
    });
    document.querySelector('#tool-count').textContent = `${count} tool${count === 1 ? '' : 's'}, ready when you are.`;
    document.querySelector('#no-tools').hidden = count > 0;
  };
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(b => {
      b.classList.toggle('selected', b === button);
      b.setAttribute('aria-pressed', String(b === button));
    });
    filter();
  }));
  search.addEventListener('input', filter);
}
const contact = document.querySelector('#contact-form');
if (contact) contact.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(contact);
  location.href = `mailto:jraymondautida@gmail.com?subject=${encodeURIComponent('Website inquiry from ' + data.get('name'))}&body=${encodeURIComponent(data.get('message') + '\n\nFrom: ' + data.get('name'))}`;
  document.querySelector('#contact-status').textContent = 'Your email app has been requested. If it does not open, email jraymondautida@gmail.com directly. Nothing has been sent by this website.';
});
