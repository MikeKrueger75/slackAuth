from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html')

@app.route('/grant')
def code():
    code = request.args['code']
    url = 'https://slack.com/api/oauth.access?client_id=14917766709.693327534246&client_secret=f844dde28cb3bad0f7f2b11f160455c7&code='+ code + '&redirect_uri=https://slack-auth.herokuapp.com/grant'
    r = requests.get(url)

    accessToken = r.json('access_token')

    return accessToken