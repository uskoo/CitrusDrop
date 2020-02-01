import json
from flask import Flask
from flask import render_template
from citrus_drop import CitrusDrop



app = Flask(__name__)

with open('./static/test2.json', encoding='utf-8') as f:
    user_info = json.load(f)

@app.route('/')
def index():
    title = "Citrus Drop"
    page = "index"
    return render_template('main.html', title=title, message=user_info, page=page)


@app.route('/donut')
def donut():
    title = "Citrus Donut"
    page = "donut"
    return render_template('donut.html', title=title, message=user_info, page=page)


if __name__ == '__main__':
    app.run()

