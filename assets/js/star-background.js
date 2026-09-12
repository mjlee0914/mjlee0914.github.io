(() => {
  "use strict";

  if (document.getElementById("star-background")) return;
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  if (!context) return;
  canvas.id = "star-background";
  canvas.setAttribute("aria-hidden", "true");
  document.body.prepend(canvas);

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const pointer = { x: 0, y: 0, active: false };
  const starShape = new Path2D();
  // Five points, alternating outer and inner radii.
  for (let i = 0; i < 10; i++) {
    const angle = i * Math.PI / 5 - Math.PI / 2;
    const radius = i % 2 ? 0.42 : 1;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    if (i === 0) starShape.moveTo(x, y);
    else starShape.lineTo(x, y);
  }
  starShape.closePath();

  let width, height, ratio, color;
  let stars = [];
  let frame = 0;
  let lastTime = 0;

  function draw(delta = 0) {
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, width, height);
    context.fillStyle = color;
    const ease = 1 - Math.exp(-delta / 140);

    stars.forEach(star => {
      // Slow upward drift; wrap outside the viewport to avoid edge flicker.
      star.y -= delta * star.speed;
      if (star.y < -8) star.y = height + 8;
      let offsetX = 0;
      let offsetY = 0;
      if (pointer.active) {
        const dx = star.x - pointer.x;
        const dy = star.y - pointer.y;
        const distance = Math.hypot(dx, dy);
        if (distance > 0 && distance < 130) {
          const push = 18 * (1 - distance / 130);
          offsetX = dx / distance * push;
          offsetY = dy / distance * push;
        }
      }
      star.offsetX += (offsetX - star.offsetX) * ease;
      star.offsetY += (offsetY - star.offsetY) * ease;
      context.save();
      context.translate(star.x + star.offsetX, star.y + star.offsetY);
      context.rotate(star.angle);
      context.scale(star.size, star.size);
      context.globalAlpha = star.opacity;
      context.fill(starShape);
      context.restore();
    });
  }

  function animate(time) {
    draw(lastTime ? Math.min(time - lastTime, 50) : 0);
    lastTime = time;
    frame = window.requestAnimationFrame(animate);
  }

  function syncAnimation() {
    window.cancelAnimationFrame(frame);
    lastTime = 0;
    pointer.active = false;
    stars.forEach(star => { star.offsetX = star.offsetY = 0; });
    if (document.hidden) return;
    draw();
    if (!reducedMotion.matches) frame = window.requestAnimationFrame(animate);
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    // Bounded density keeps mobile and large displays inexpensive.
    const count = Math.min(60, Math.max(16, Math.round(width * height / 22000)));
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      size: 2.5 + Math.random() * 2,
      angle: Math.random() * Math.PI,
      opacity: 0.18 + Math.random() * 0.18,
      speed: 0.003 + Math.random() * 0.005,
      offsetX: 0,
      offsetY: 0
    }));
    syncAnimation();
  }

  function updateColor() {
    color = window.getComputedStyle(canvas).color;
    if (!document.hidden) draw();
  }

  window.addEventListener("pointermove", event => {
    pointer.active = finePointer.matches && !reducedMotion.matches && event.pointerType === "mouse";
    pointer.x = event.clientX;
    pointer.y = event.clientY;
  }, { passive: true });
  document.addEventListener("pointerleave", () => { pointer.active = false; });
  window.addEventListener("blur", () => { pointer.active = false; });
  window.addEventListener("resize", resize, { passive: true });
  document.addEventListener("visibilitychange", syncAnimation);
  reducedMotion.addEventListener("change", syncAnimation);
  finePointer.addEventListener("change", () => { pointer.active = false; });
  new MutationObserver(updateColor).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"]
  });

  color = window.getComputedStyle(canvas).color;
  resize();
})();
