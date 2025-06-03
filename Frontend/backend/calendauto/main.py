from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    selected_options = request.form.getlist('materias_check')
    print(f"Selected Options: {selected_options}")
    # Process the selected options
    return selected_options

if __name__ == '__main__':
    app.run(debug=True)
