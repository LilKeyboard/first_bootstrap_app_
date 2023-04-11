from flask import Flask, render_template

#testowy commit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
