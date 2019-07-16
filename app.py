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
    #Access-Tokens Lesen
    accessTokens = {}
    action="geladen: "
    userId = request.args.get('userid')

    code = request.args.get('code')
    if(code):
        # Access-Token holen
        url = 'https://slack.com/api/oauth.access?client_id=14917766709.693327534246&client_secret=f844dde28cb3bad0f7f2b11f160455c7&code='+ code + '&redirect_uri=https://slack-auth.herokuapp.com/grant'
        r = requests.get(url)
        rjson = json.loads(r.text)
        accessToken = rjson['access_token']
        # Todo: Access-Token speichern

        userId = accessToken[-20:]
        data = {userId: accessToken}
        accessTokens.update(data)

        # Speichern
        f = open("data.bin", "wb")
        pickle.dump(accessTokens, f)
        f.close()

        action="neu: "

    if(userId):
        # Access-Token auslesen
        try:
            with open("data.bin", "rb") as f:
                accessTokens = pickle.load(f)
                f.close()
                accessToken = accessTokens[userId]
        except:
            print("Datei data.bin nicht gefunden.")


    if(accessToken):
        # User identifizieren
        header = {
                'Authorization': 'Bearer ' + accessToken
            }
        url = 'https://slack.com/api/auth.test'
        r = requests.get(url, headers=header)
        user = json.loads(r.text)['user_id']
        username = json.loads(r.text)['user']


        return render_template('install_ready.html', userId=userId, username=username)
    else:
        return render_template('install.html')

@app.route('/setstate')
def setstate():
    userId = request.args.get('userid')

    if (userId):
        # Access-Token auslesen
        try:
            with open("data.bin", "rb") as f:
                accessTokens = pickle.load(f)
                f.close()
                accessToken = accessTokens[userId]
        except:
            print("FEHLER: Datei data.bin nicht gefunden.")

    if (accessToken):
        # User-Profile Status setzen
        header = {
            'Authorization': 'Bearer ' + accessToken,
            'Content-type': 'application/json; charset=utf-8'
        }
        url = 'https://slack.com/api/users.profile.set'
        data = {
            "profile": {
                "status_text": request.args.get('status_text'),
                "status_emoji": request.args.get('status_emoji')
            }
        }
        r = requests.post(url=url, data=json.dumps(data), headers=header)
        return str(data)
    else:
        return "FEHLER: Es konnte kein Access_Token ermittelt werden."