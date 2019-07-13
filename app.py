from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html')

@app.route('/grant')
def code():
    # Access-Token holen
    code = request.args['code']
    url = 'https://slack.com/api/oauth.access?client_id=14917766709.693327534246&client_secret=f844dde28cb3bad0f7f2b11f160455c7&code='+ code + '&redirect_uri=https://slack-auth.herokuapp.com/grant'
    r = requests.get(url)
    rjson = json.loads(r.text)
    accessToken = rjson['access_token']
    # Todo: Access-Token speichern

    # User identifizieren
    header = headers = {
        'Authorization': 'Bearer ' + accessToken
    }
    url = 'https://slack.com/api/auth.test'
    r = requests.get(url, headers=header)
    user = json.loads(r.text)['user_id']

    # User-Profile Status setzen
    header = headers = {
            'authorization': 'Bearer '+accessToken
        }
    url = 'https://slack.com/api/users.profile.set'
    params = {'user': user, 'name' : 'status_text', 'value' : 'Slack-App was here'}
    r = requests.post(url=  url,params =params, headers = header)

    return 'Ready...'