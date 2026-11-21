
const canvas = document.getElementById("background-canvas");
const ctx = canvas.getContext("2d");

let width;
let height;
let particles = [];

const spacing = 35;
const mouse = { x: -1000, y: -1000 };

function resizeCanvas() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    width = window.innerWidth;
    height = window.innerHeight;

    canvas.width = width * dpr;
    canvas.height = height * dpr;

    canvas.style.width = width + "px";
    canvas.style.height = height + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    createParticles();
}

function createParticles() {
    particles = [];

    for (let x = -spacing; x < width + spacing; x += spacing) {
        for (let y = -spacing; y < height + spacing; y += spacing) {
            particles.push({
                x: x,
                y: y,
                baseX: x,
                baseY: y,
                phase: Math.random() * Math.PI * 2
            });
        }
    }
}

window.addEventListener("resize", resizeCanvas);

window.addEventListener("mousemove", (event) => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
});

window.addEventListener("mouseout", (event) => {
    if (!event.relatedTarget) {
        mouse.x = -1000;
        mouse.y = -1000;
    }
});

function animate() {
    ctx.clearRect(0, 0, width, height);

    const time = performance.now() * 0.0005;

    // Nuqtalarni harakatlantirish
    particles.forEach((p) => {
        const wave = Math.sin(
            p.baseX * 0.008 + time + p.phase
        ) * 12;

        const wave2 = Math.cos(
            p.baseY * 0.009 + time + p.phase
        ) * 10;

        let targetX = p.baseX + wave;
        let targetY = p.baseY + wave2;

        const dx = mouse.x - targetX;
        const dy = mouse.y - targetY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 170) {
            const force = (170 - distance) / 170;

            targetX -= dx * force * 0.45;
            targetY -= dy * force * 0.45;
        }

        p.x += (targetX - p.x) * 0.08;
        p.y += (targetY - p.y) * 0.08;
    });

    // Nuqtalar orasidagi chiziqlar
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const a = particles[i];
            const b = particles[j];

            const dx = a.x - b.x;
            const dy = a.y - b.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < spacing * 1.55) {
                const opacity = (1 - distance / (spacing * 1.55)) * 0.22;

                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);

                ctx.strokeStyle = `rgba(80, 80, 80, ${opacity})`;
                ctx.lineWidth = 0.7;
                ctx.stroke();
            }
        }
    }

    // Nuqtalarni chizish
    particles.forEach((p) => {
        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        const radius = distance < 170 ? 2.2 : 1.4;

        ctx.beginPath();
        ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);

        ctx.fillStyle = distance < 170
            ? "rgba(40, 40, 40, 0.65)"
            : "rgba(70, 70, 70, 0.30)";

        ctx.fill();
    });

    requestAnimationFrame(animate);
}

resizeCanvas();
animate();
