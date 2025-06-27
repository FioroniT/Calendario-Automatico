import os
from flask import Flask, render_template, request
import json
from os import listdir
from os.path import isfile, join
app = Flask(__name__)

def get_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        fileData = json.load(f)
        f.close()
        return fileData

@app.route('/')
def index():
    fileData = get_links(os.path.join(os.path.dirname(__file__), '../../../Outputs', 'links_completo_prueba.json'))
    return render_template('index.html', fileData = fileData)

@app.route('/submit', methods=['POST'])
def submit():
    selected_options = request.form.getlist('materias_check')
    selected_carrera = request.form.get('carreraElegida')
    print(f"Selected Options: {selected_options}")
    materias = []
    comisiones = []
    for materia in selected_options:
        materias.append(materia.split(':')[0])
        comisiones.append(materia.split(':')[1])
   
    
    complete_data = list(zip(materias, comisiones))
    carreraData = 0
    links = []
    links_path = os.path.join(os.path.dirname(__file__), '../../../Outputs', 'links_completo_prueba.json')
    
    with open(links_path, 'r', encoding='utf-8') as f:
        carreraData = json.load(f)
        f.close()
    
    
    for data in complete_data:
        links.append(carreraData.get(selected_carrera, {}).get(data[0], {}).get(data[1], {}).get("link"))

    links.append(carreraData.get("Calendario Academico",{}).get("link"))
    selected_options.append("Calendario Academico")
    #selected_options.append(selected_carrera)

    botones = zip(selected_options, links)
    return render_template('botones.html', botones=botones)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

