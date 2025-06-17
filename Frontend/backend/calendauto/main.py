import os
from flask import Flask, render_template, request
import json
from os import listdir
from os.path import isfile, join
app = Flask(__name__)

@app.route('/')
def index():
    outputs_dir = os.path.join(os.path.dirname(__file__), 'static', 'Outputs')
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    filesData = [f for f in listdir(outputs_dir) if isfile(join(outputs_dir, f))]
    fileData = {}
    j = 0
    for i in filesData:
        with open(os.path.join(outputs_dir, i), 'r', encoding='utf-8') as f:
            fileData[j]= json.load(f)
            f.close()
        j=j+1

    return render_template('index.html',  filesData = filesData, fileData = fileData)

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
    links_path = os.path.join(os.path.dirname(__file__), 'static', 'links.json')
    
    with open(links_path, 'r', encoding='utf-8') as f:
        carreraData = json.load(f)
        f.close()
    
    for data in complete_data:
        links.append(carreraData.get(selected_carrera, {}).get(data[0], {}).get(data[1], {}).get("link"))

    #selected_options.append(selected_carrera)

    botones = zip(selected_options, links)
    return render_template('botones.html', botones=botones)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
