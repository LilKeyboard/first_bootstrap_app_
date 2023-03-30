from flask import Flask, render_template
from flask_bootstrap import Bootstrap

#testowy commit

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')
