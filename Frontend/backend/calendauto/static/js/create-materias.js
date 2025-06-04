function generateMaterias(i) {  
  const data = materias_source[i]; 
  createMateriasButtons(data);
};

function createMateriasButtons(data) {
  const carreras_obj = data;
  const materias_container = document.getElementById('materias-content');
  let i = 0;
  for (let x in carreras_obj) {
    let arr = [];
    for(let j = 0; j<carreras_obj[x].horarios.length;j++){
      if(!arr.includes(carreras_obj[x].horarios[j].comision)){
        arr.push(carreras_obj[x].horarios[j].comision);
      }
    };
    for(let j = 0; j<arr.length; j++){
      var tr = document.createElement('tr');
      var td = document.createElement('td');
      const button = document.createElement('button');
      button.className = "materia-button";
      button.type = "button";

      if((i == (Object.keys(carreras_obj).length)-1) && (j==arr.length-1)){
        button.style.borderRadius = "1px 1px 15px 15px";
      }

      const checkBox = document.createElement('input');
      checkBox.type = 'checkbox';
      checkBox.name = 'materias_check';
      checkBox.value = x+":"+arr[j];
      
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
      com.innerText = arr[j];
      td.appendChild(com);
      button.appendChild(td);
      tr.appendChild(button);    
       
      materias_container.appendChild(tr);
    }
    i = i+1;
    
  }
  
}




