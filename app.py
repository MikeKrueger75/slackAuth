from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html')

@app.route('/grant')
def code():
    code = request.args['code']
    r = requests.get('http://httpbin.org/status/418')
    return HttpResponse("Authorization Grant=" + code + '</p><pre>' + r.text + '</pre>')