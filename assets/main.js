// Reveal sections as they enter the viewport
const io = 'IntersectionObserver' in window && new IntersectionObserver((entries) => {
  entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.rail > section').forEach((s) => io ? io.observe(s) : s.classList.add('in'));
document.documentElement.classList.add('js');
