
const container = document.getElementById('dpdw-carreras');

var formDiv = document.getElementById('materias-content');
const button = document.createElement('button');
button.innerText = "Ingenieria en Computacion";
button.addEventListener('click', function() {
  changeCarrera("Ingenieria en Computacion");
  formDiv.innerHTML = '';
  generateMaterias();
  showMaterias();
  dropDownCarreras();
});
container.appendChild(button);
