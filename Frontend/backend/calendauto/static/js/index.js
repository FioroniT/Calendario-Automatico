var flag_carrera = 0;
const carreras_obj = materias_source;//JSON.parse(json_text);

function dropDownCarreras() {
  document.getElementById("dpdw-carreras").classList.toggle("show");
}

function changeCarrera(carrera){
  document.getElementById("carreras-btn").innerText = carrera;
}

function showMaterias() {
  document.getElementById("holder-id").classList.toggle("show", flag_carrera == 0);
  
}
