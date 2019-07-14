from flask import Flask, render_template, request
import requests
import json
import pickle

app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html')

@app.route('/grant')
def grant():
    #f = file("tokens.bin", "rb")
    #accessTokens = pickle.load(f)

    code = request.args['code']
    if(code.strip()):
        # Access-Token holen
        url = 'https://slack.com/api/oauth.access?client_id=14917766709.693327534246&client_secret=f844dde28cb3bad0f7f2b11f160455c7&code='+ code + '&redirect_uri=https://slack-auth.herokuapp.com/grant'
        r = requests.get(url)
        rjson = json.loads(r.text)
        accessToken = rjson['access_token']
        # Todo: Access-Token speichern

    userId=accessToken[-10:]

    print(userId)
    print(accessToken)
    data={userId : accessToken}
    print(data)
    #pickle.dump(accessTokens.update(data), f)
    #f.close()

    # userId = request.args['userid']
    # if(userId.strip()):
    #     # Access-Token auslesen
    #     return "userId=" + userId

    if(accessToken.strip()):
        # User identifizieren
        header = {
                'Authorization': 'Bearer ' + accessToken
            }
        url = 'https://slack.com/api/auth.test'
        r = requests.get(url, headers=header)
        user = json.loads(r.text)['user_id']

        # User-Profile Status setzen
        header = {
                'Authorization': 'Bearer '+accessToken,
                'Content-type' : 'application/json; charset=utf-8'
            }
        url = 'https://slack.com/api/users.profile.set'
        data = {
            "profile": {
                "status_text": "riding a train",
                "status_emoji": ":mountain_railway:"
            }
        }
        r = requests.post(url = url, data = json.dumps(data), headers = header)
        return data
    else:
        return render_template('install.html')
