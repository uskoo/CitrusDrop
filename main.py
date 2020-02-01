from flask import Flask
from flask import render_template
from citrus_drop import CitrusDrop


app = Flask(__name__)

@app.route('/')
def index():
    title = "Citrus Drop"
    message = "test"
    return render_template('main.html', message=message, title=title)

@app.route('/donut')
def donut():
    title = "Citrus Donut"
    message = "Donut"
    return render_template('donut.html', message=message, title=title)


if __name__ == '__main__':
    app.run()

