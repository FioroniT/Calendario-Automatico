from flask import Flask, render_template, request
import json
from os import listdir
from os.path import isfile, join
app = Flask(__name__)

@app.route('/')
def index():
    filesData = [f for f in listdir("./static/Outputs/") if isfile(join("./static/Outputs/", f))]
    fileData = {}
    j = 0
    for i in filesData:
        with open('./static/Outputs/'+i, 'r') as f:
            fileData[j]= json.load(f)
            f.close()
        j=j+1

    return render_template('index.html',  filesData = filesData, fileData = fileData)

@app.route('/submit', methods=['POST'])
def submit():
    selected_options = request.form.getlist('materias_check')
    selected_carrera = request.form.get('carreraElegida')
    print(f"Selected Options: {selected_options}")
    # Process the selected options
    materias = []
    comisiones = []
    i = 0
    for materia in selected_options:
        materias.append(materia.split(':')[0])
        comisiones.append(materia.split(':')[1])
        i=i+1
    
    complete_data = list(zip(materias, comisiones))
    carreraData = 0
    links = []
    with open('./static/links.json', 'r') as f:
        carreraData = json.load(f);
        f.close();
    
    for data in complete_data:
        links.append(carreraData.get(selected_carrera, {}).get(data[0], {}).get(data[1]).get("link"))

    selected_options.append(selected_carrera)
    return links

if __name__ == '__main__':
    app.run(debug=True)
