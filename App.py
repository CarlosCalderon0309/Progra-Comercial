from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    IMC = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        IMC = weight / (height ** 2)
    return render_template('pag.html', IMC=IMC)

if __name__ == '__main__':
    app.run(debug=True)
