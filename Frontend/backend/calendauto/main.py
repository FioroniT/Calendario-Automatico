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
    print(f"Selected Options: {selected_options}")
    # Process the selected options
    return selected_options

if __name__ == '__main__':
    app.run(debug=True)
