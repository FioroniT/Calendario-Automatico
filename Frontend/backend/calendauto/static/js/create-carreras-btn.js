
const container = document.getElementById('dpdw-carreras');

var formDiv = document.getElementById('materias-content');
for(let i = 0; i<carreras_source.length; i++){  
  const button = document.createElement('button');
  button.innerText = carreras_source[i];
  button.addEventListener('click', function() {
    changeCarrera(carreras_source[i]);
    document.getElementById('carreraElegida').value = carreras_source[i];
    formDiv.innerHTML = '';
    generateMaterias(i);
    showMaterias();
    dropDownCarreras();
  });
  container.appendChild(button);
};
