
const container = document.getElementById('dpdw-carreras');

for (let i = 1; i <= 5; i++) {
  const button = document.createElement('button');
  button.innerHTML = `Button ${i}`;
  button.addEventListener('click', function() {
    changeCarrera(button.innerHTML);
  });
  container.appendChild(button);
}
