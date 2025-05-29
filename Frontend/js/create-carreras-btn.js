
const container = document.getElementById('dpdw-carreras');


for (let i = 0; i < carreras_obj.carreras.length; i++) {
  const button = document.createElement('button');
  button.innerHTML = carreras_obj.carreras[i].nombre;
  button.addEventListener('click', function() {
    changeCarrera(carreras_obj.carreras[i].nombre);
    seleccion_carrera = i;
  });
  container.appendChild(button);
}
