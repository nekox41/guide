import { startPetals } from './effects/petals.js';

const root = document.documentElement;
const store = (key,value) => { try { localStorage.setItem(key,value); } catch {} };
const refreshPetals = startPetals();
const themeButton = document.querySelector('[data-theme-toggle]');
const effectButton = document.querySelector('[data-effects-toggle]');
function syncButtons() {
  const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  themeButton.setAttribute('aria-label', dark ? '切换浅色主题' : '切换深色主题');
  effectButton.setAttribute('aria-pressed', String(root.dataset.effects !== 'off'));
}
themeButton.addEventListener('click', () => {
  const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = dark ? 'light' : 'dark';
  store('aa-theme', root.dataset.theme);
  syncButtons();
});
effectButton.addEventListener('click', () => {
  root.dataset.effects = root.dataset.effects === 'off' ? 'on' : 'off';
  store('aa-effects', root.dataset.effects);
  refreshPetals();
  syncButtons();
});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', syncButtons);
syncButtons();

const menu = document.querySelector('[data-menu]');
const desktop = matchMedia('(min-width: 1024px)');
function syncMenu() { menu.open = desktop.matches; }
desktop.addEventListener('change', syncMenu);
syncMenu();

const dialog = document.querySelector('[data-search-dialog]');
const input = document.querySelector('#search-input');
const results = document.querySelector('.aa-results');
const status = document.querySelector('.aa-search__status');
let index;
let loading;
async function loadIndex() {
  if (!loading) loading = fetch('/search-index.json', {cache:'no-cache'}).then(response => {
    if (!response.ok) throw new Error('index');
    return response.json();
  }).catch(error => { loading = null; throw error; });
  index = await loading;
}
async function search() {
  const query = input.value.trim().toLocaleLowerCase();
  results.replaceChildren();
  if (!query) { status.textContent = '输入关键词，寻找你需要的那一页。'; return; }
  status.textContent = '正在查找书页……';
  try { await loadIndex(); } catch { status.textContent = '搜索暂时无法加载，请稍后重试。'; return; }
  if (query !== input.value.trim().toLocaleLowerCase()) return;
  const words = query.split(/\s+/);
  const matches = index.filter(page => words.every(word => (page.title+' '+page.text).toLocaleLowerCase().includes(word)))
    .sort((a,b) => Number(b.title.toLocaleLowerCase().includes(query))-Number(a.title.toLocaleLowerCase().includes(query)));
  status.textContent = matches.length ? `找到 ${matches.length} 页，显示前 ${Math.min(matches.length,20)} 页。` : '暂时没有找到，换个关键词试试？';
  for (const page of matches.slice(0,20)) {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = page.url;
    const heading = document.createElement('strong');
    heading.textContent = page.title;
    const excerpt = document.createElement('p');
    const position = Math.max(0,page.text.toLocaleLowerCase().indexOf(words[0])-24);
    excerpt.textContent = page.text.slice(position,position+100)+'……';
    a.append(heading,excerpt); li.append(a); results.append(li);
  }
}
document.querySelector('[data-search-open]').addEventListener('click', () => { dialog.showModal(); input.focus(); });
document.querySelector('[data-search-close]').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom) dialog.close(); } });
input.addEventListener('input', search);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && dialog.open) { event.preventDefault(); dialog.close(); }
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); if(!dialog.open)dialog.showModal(); input.focus(); }
});

document.querySelectorAll('[data-video-load]').forEach(button => button.addEventListener('click', () => {
  const card = button.closest('[data-video]');
  const frame = document.createElement('iframe');
  frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(card.dataset.video)}`;
  frame.title = '本节视频教程（YouTube）';
  frame.allowFullscreen = true;
  frame.loading = 'lazy';
  card.dataset.loaded = '';
  card.replaceChildren(frame);
}));

let queued = false;
function progress() {
  if (queued) return;
  queued = true;
  requestAnimationFrame(() => {
    const length = root.scrollHeight-innerHeight;
    root.style.setProperty('--aa-progress', length>0 ? String(Math.min(1,scrollY/length)) : '0');
    queued = false;
  });
}
addEventListener('scroll',progress,{passive:true});
addEventListener('resize',progress);
progress();
const tocLinks = [...document.querySelectorAll('.aa-toc a[href^="#"]')];
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) if(entry.isIntersecting) {
    tocLinks.forEach(a => { if(a.hash === '#'+entry.target.id)a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); });
  }
},{rootMargin:'-15% 0px -65% 0px'});
document.querySelectorAll('.aa-article h2[id]').forEach(h=>observer.observe(h));

// 原画只做容器浮动，不对单张图片模拟眼、耳、尾巴变形。
function visibility() { root.toggleAttribute('data-page-hidden',document.hidden); }
document.addEventListener('visibilitychange',visibility);
visibility();
