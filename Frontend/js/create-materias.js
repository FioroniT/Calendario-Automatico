const materias_container = document.getElementById('materias-content');

for (let i = 0; i < carreras_obj.carreras[seleccion_carrera].materias.length; i++) {
  var tr = document.createElement('tr');
  var td = document.createElement('td');

  const checkBox = document.createElement('input');
  checkBox.type = 'checkbox';
  td.appendChild(checkBox);
  tr.appendChild(td);

  td = document.createElement('td');
  const nombre = document.createElement('label');
  nombre.innerText = carreras_obj.carreras[seleccion_carrera].materias[i].nombre;
  td.appendChild(nombre);
  tr.appendChild(td);

  td = document.createElement('td');
  const com = document.createElement('label');
  com.innerText = carreras_obj.carreras[seleccion_carrera].materias[i].comision;
  td.appendChild(com);
  tr.appendChild(td);
  
  materias_container.appendChild(tr);
}




