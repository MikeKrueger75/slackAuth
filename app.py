from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Mike!'

@app.route('/form')
def form():
    return render_template('form.html', name="Mike")

@app.route('/result', methods=['get', 'post'])
def result():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    gender = request.form['gender']

    return "Thank you " + firstname + " " + lastname + " ("+ gender +")!"
