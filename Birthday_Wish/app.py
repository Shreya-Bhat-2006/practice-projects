from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def birthday():
    if request.method == 'POST':
        name = request.form['name']
        return render_template('wish.html', name=name)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
