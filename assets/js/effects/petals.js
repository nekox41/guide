// 粒子数量克制，动态偏好改变后重建，切到后台时由全局状态暂停。
export function startPetals() {
  const root = document.documentElement;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 768px)');
  let layer;
  function refresh() {
    layer?.remove();
    if (motion.matches || root.dataset.effects === 'off') return;
    layer = document.createElement('div');
    layer.className = 'aa-fx';
    layer.setAttribute('aria-hidden', 'true');
    const count = mobile.matches ? 8 : 16;
    for (let i = 0; i < count; i++) {
      const petal = document.createElement('i');
      petal.className = 'aa-petal';
      if (i % 4 === 3) petal.dataset.blue = '';
      petal.style.setProperty('--aa-left', `${Math.random() * 100}%`);
      petal.style.setProperty('--aa-petal-size', `${9 + Math.random() * 5}px`);
      petal.style.setProperty('--aa-petal-duration', `${10 + Math.random() * 4}s`);
      petal.style.setProperty('--aa-petal-delay', `${-Math.random() * 14}s`);
      petal.style.setProperty('--aa-sway', `${24 + Math.random() * 16}px`);
      layer.append(petal);
    }
    document.body.append(layer);
  }
  motion.addEventListener('change', refresh);
  mobile.addEventListener('change', refresh);
  refresh();
  return refresh;
}
