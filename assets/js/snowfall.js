(() => {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reducedMotion.matches || document.getElementById("snowfall")) return;

  const canvas = document.createElement("canvas");
  canvas.id = "snowfall";
  canvas.setAttribute("aria-hidden", "true");
  document.body.appendChild(canvas);

  const context = canvas.getContext("2d");
  if (!context) {
    canvas.remove();
    return;
  }

  let width = 0;
  let height = 0;
  let flakes = [];
  let animationFrame = 0;
  let lastTime = performance.now();

  const createFlake = (randomY = true) => ({
    x: Math.random() * width,
    y: randomY ? Math.random() * height : -12,
    radius: 1.2 + Math.random() * 2.4,
    speed: 16 + Math.random() * 28,
    drift: -5 + Math.random() * 10,
    phase: Math.random() * Math.PI * 2,
    opacity: 0.26 + Math.random() * 0.34,
  });

  const resize = () => {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    const flakeCount = Math.min(64, Math.max(26, Math.round((width * height) / 26000)));
    flakes = Array.from({ length: flakeCount }, () => createFlake());
  };

  const draw = (time) => {
    const elapsed = Math.min((time - lastTime) / 1000, 0.05);
    lastTime = time;
    context.clearRect(0, 0, width, height);

    const isDark = document.documentElement.dataset.theme === "dark";
    const color = isDark ? "218, 227, 247" : "95, 117, 184";

    flakes.forEach((flake) => {
      flake.phase += elapsed * 0.9;
      flake.x += (flake.drift + Math.sin(flake.phase) * 7) * elapsed;
      flake.y += flake.speed * elapsed;

      if (flake.y > height + 12 || flake.x < -16 || flake.x > width + 16) {
        Object.assign(flake, createFlake(false));
      }

      context.beginPath();
      context.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
      context.fillStyle = `rgba(${color}, ${flake.opacity})`;
      context.fill();
    });

    animationFrame = requestAnimationFrame(draw);
  };

  const handleVisibility = () => {
    cancelAnimationFrame(animationFrame);
    if (!document.hidden) {
      lastTime = performance.now();
      animationFrame = requestAnimationFrame(draw);
    }
  };

  resize();
  animationFrame = requestAnimationFrame(draw);
  window.addEventListener("resize", resize, { passive: true });
  document.addEventListener("visibilitychange", handleVisibility);
})();
