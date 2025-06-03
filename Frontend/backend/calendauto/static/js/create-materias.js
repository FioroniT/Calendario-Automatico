function generateMaterias() {  
  const materias_container = document.getElementById('materias-content');

  let i = 0;
  for (let x in carreras_obj) {
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    const button = document.createElement('button');
    button.className = "materia-button";
    button.type = "button";

    if(i == (Object.keys(carreras_obj).length)-1){
      button.style.borderRadius = "1px 1px 15px 15px";
    }

    const checkBox = document.createElement('input');
    checkBox.type = 'checkbox';
    checkBox.name = 'materias_check';
    checkBox.value = x;
    
    button.addEventListener('click', function() {
      checkBox.click();
    });

    td.appendChild(checkBox);
    button.appendChild(td);
    tr.appendChild(button);

    td = document.createElement('td');
    const nombre = document.createElement('p');
    nombre.innerText = x;
    td.appendChild(nombre);
    button.appendChild(td);
    tr.appendChild(button);

    td = document.createElement('td');
    const com = document.createElement('p');
    com.innerText = carreras_obj[x].horarios[0].comision;
    td.appendChild(com);
    button.appendChild(td);
    tr.appendChild(button);
    
    
    i = i+1;
    materias_container.appendChild(tr);
  }
}




