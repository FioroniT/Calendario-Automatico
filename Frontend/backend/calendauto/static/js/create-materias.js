function generateMaterias(ncarrera) {  
  const materias_container = document.getElementById('materias-content');

  for (let i = 0; i < carreras_obj.carreras[ncarrera].materias.length; i++) {
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    const button = document.createElement('button');
    button.className = "materia-button";
    button.type = "button";

    if(i == (carreras_obj.carreras[ncarrera].materias.length-1)){
      button.style.borderRadius = "1px 1px 15px 15px";
    }

    const checkBox = document.createElement('input');
    checkBox.type = 'checkbox';
    checkBox.name = 'materias_check';
    checkBox.value = carreras_obj.carreras[ncarrera].materias[i].nombre;
    
    button.addEventListener('click', function() {
      checkBox.click();
    });

    td.appendChild(checkBox);
    button.appendChild(td);
    tr.appendChild(button);

    td = document.createElement('td');
    const nombre = document.createElement('p');
    nombre.innerText = carreras_obj.carreras[ncarrera].materias[i].nombre;
    td.appendChild(nombre);
    button.appendChild(td);
    tr.appendChild(button);

    td = document.createElement('td');
    const com = document.createElement('p');
    com.innerText = carreras_obj.carreras[ncarrera].materias[i].comision;
    td.appendChild(com);
    button.appendChild(td);
    tr.appendChild(button);
    
    
    materias_container.appendChild(tr);
  }
}




