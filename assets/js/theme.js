// 首屏前读取偏好，避免明暗主题闪烁；存储不可用时跟随系统。
try {
  const theme = localStorage.getItem('aa-theme');
  if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
  if (localStorage.getItem('aa-effects') === 'off') document.documentElement.dataset.effects = 'off';
} catch {}
