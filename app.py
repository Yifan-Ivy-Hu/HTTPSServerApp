from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        key = request.form["key"]
        value = request.form["value"]
        print("!!!", request.form)
    return render_template('homepage.html')