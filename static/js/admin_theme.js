// Highlight current nav link
document.querySelectorAll('#nav-sidebar a').forEach(a => {
  if (a.href === location.href || location.pathname.startsWith(a.pathname) && a.pathname !== '/admin/') {
    a.style.background = 'rgba(59,130,246,.18)';
    a.style.color = '#60a5fa';
  }
});
