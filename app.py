from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html')

@app.route('/grant')
def token():
    code = request.args['code']
    return "Authorization Grant=" + code

@app.route('/token')
def token():
    data = request.data
    dataDict = json.loads(data)
    token = dataDict['access_token']
    return token
