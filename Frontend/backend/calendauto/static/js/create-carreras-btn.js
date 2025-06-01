
const container = document.getElementById('dpdw-carreras');

var formDiv = document.getElementById('materias-content');
for (let i = 0; i < carreras_obj.carreras.length; i++) {
  const button = document.createElement('button');
  button.innerText = carreras_obj.carreras[i].nombre;
  button.addEventListener('click', function() {
    changeCarrera(carreras_obj.carreras[i].nombre);
    formDiv.innerHTML = '';
    generateMaterias(i);
    showMaterias();
    dropDownCarreras();
  });
  container.appendChild(button);
}
