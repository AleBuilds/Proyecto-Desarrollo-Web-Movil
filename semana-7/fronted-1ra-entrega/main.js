// El Mediterráneo — interacciones básicas del wireframe (ES6)

document.addEventListener('DOMContentLoaded', () => {
  // Menú móvil
  const toggle = document.querySelector('.navbar-toggle');
  const links = document.querySelector('.navbar-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const abierto = links.classList.toggle('navbar-links-abierto');
      toggle.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
  }

  // Steppers de cantidad (producto, carrito)
  const steppers = document.querySelectorAll('.stepper');
  steppers.forEach((stepper) => {
    const input = stepper.querySelector('input');
    const [btnMenos, btnMas] = stepper.querySelectorAll('button');
    if (!input) return;

    btnMenos?.addEventListener('click', () => {
      const valor = parseInt(input.value, 10) || 1;
      input.value = Math.max(1, valor - 1);
    });

    btnMas?.addEventListener('click', () => {
      const valor = parseInt(input.value, 10) || 1;
      input.value = valor + 1;
    });
  });
});
