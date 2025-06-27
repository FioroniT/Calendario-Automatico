function generateMaterias(i) {  
  const data = json_source[i]; 
  createMateriasButtons(data);
};


function createMateriasButtons(carrera) {
  const materias_container = document.getElementById('materias-content');
  let i = 0;
  let j = 0;
  for (let materia in carrera) {
    for(let comision in carrera[materia]) {
      var tr = document.createElement('tr');
      var td = document.createElement('td');
      const button = document.createElement('button');
      button.className = "materia-button";
      button.type = "button";

      if((i == (Object.keys(carrera).length)-1) && (j==Object.keys(carrera[materia]).length-1)){
        button.style.borderRadius = "1px 1px 15px 15px";
      }

      const checkBox = document.createElement('input');
      checkBox.type = 'checkbox';
      checkBox.name = 'materias_check';
      checkBox.value = materia+":"+comision;
      
      button.addEventListener('click', function() {
        checkBox.click();
      });

      td.appendChild(checkBox);
      button.appendChild(td);
      tr.appendChild(button);

      td = document.createElement('td');
      const nombre = document.createElement('p');
      nombre.innerText = materia;
      td.appendChild(nombre);
      button.appendChild(td);
      tr.appendChild(button);

      td = document.createElement('td');
      const com = document.createElement('p');
      com.innerText = comision;
      td.appendChild(com);
      button.appendChild(td);
      tr.appendChild(button);    
      
      materias_container.appendChild(tr);
      j = j+1;
    }    
    j = 0;
    i = i+1;  
  }
}




