from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route('/')
def index():
    fileData = 0;
    with open('data.json', 'r') as f:
        fileData = json.load(f)
        f.close()
    return render_template('index.html', fileData = fileData)

@app.route('/submit', methods=['POST'])
def submit():
    selected_options = request.form.getlist('materias_check')
    print(f"Selected Options: {selected_options}")
    # Process the selected options
    return selected_options

if __name__ == '__main__':
    app.run(debug=True)
