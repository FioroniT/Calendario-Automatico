var seleccion_carrera = 1;

let json_text = '{"carreras" : [' +
'{"nombre" : "Ingenieria en Computacion",'+
'"materias" : [' +
'{ "nombre":"B600-Matematica I" , "comision":"C1" },' +
'{ "nombre":"B601-Introduccion Ingenieria en Computacion" , "comision":"C1" },' +
'{ "nombre":"B600-Matematica I" , "comision":"C2" } ]},'+
'{"nombre" : "Ingenieria en Electronica",'+
'"materias" : [' +
'{ "nombre":"E500-Analisis Matematico" , "comision":"C1" },' +
'{ "nombre":"E501-Analisis Matematico" , "comision":"C2" } ]}'+
']}';

const carreras_obj = JSON.parse(json_text);

function dropDown() {
  document.getElementById("dpdw-carreras").classList.toggle("show");
}

function changeCarrera(carrera){
  document.getElementById("carreras-btn").innerText = carrera;
}
