var formDiv = document.getElementById('materias-content');
const container = document.getElementById('dpdw-carreras'); //Obtengo el contenedor de los botones
delete json_source['Calendario Academico'];
const carreras = json_source; //Obtengo todas las carreras y omito el Calendario Academico

for(let carrera in carreras){ //Recorro todas las carreras que hay en el json
  const button = document.createElement('button'); //Creo un boton
  button.innerText = carrera; //Asigno el nombre de la carrera al boton
  button.addEventListener('click', function() {
    document.getElementById('carreraElegida').value = carrera; //Variable fantasma para saber que carrera se eligio en el flask
    formDiv.innerHTML = ''; //Vacio el formulario que contiene las materias
    //create-materias.js
    generateMaterias(carrera); //Genero las materias de la carrera
    //index.js
    changeCarrera(carrera); //Cambio el contenido del boton dropdown
    showMaterias(); //Las muesto
    dropDownCarreras(); 
  });
  container.appendChild(button);
   
 
