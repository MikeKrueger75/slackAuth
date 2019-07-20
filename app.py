from flask import Flask, render_template, request
import requests
import json
import pickle

app = Flask(__name__)

@app.route('/')
def install():
    return render_template('install.html', error="none", error_text="")

@app.route('/grant')
def grant():
    #Access-Tokens Lesen
    accessTokens = {}
    install = "false"
    userId = request.args.get('userid')

    code = request.args.get('code')
    if(code):
        # Access-Token holen
        url = 'https://slack.com/api/oauth.access?client_id=14917766709.693327534246&client_secret=f844dde28cb3bad0f7f2b11f160455c7&code='+ code + '&redirect_uri=https://slack-auth.herokuapp.com/grant'
        r = requests.get(url)
        rjson = json.loads(r.text)
        accessToken = rjson['access_token']

        userId = accessToken[-20:]
        data = {userId: accessToken}
        accessTokens.update(data)

        # Speichern
        f = open("data.bin", "wb")
        pickle.dump(accessTokens, f)
        f.close()
        install = "true"

    if(userId):
        # Access-Token auslesen
        try:
            with open("data.bin", "rb") as f:
                accessTokens = pickle.load(f)
                f.close()
                accessToken = accessTokens[userId]
        except:
            return render_template('install.html', error="true", error_text="(could not load access-token-1)")

        if(accessToken):
            # User identifizieren
            header = {
                    'Authorization': 'Bearer ' + accessToken
                }
            url = 'https://slack.com/api/auth.test'
            r = requests.get(url, headers=header)
            username = json.loads(r.text)['user']

            if(install == "true"):
                return render_template('tryout.html',
                                       msg_type="success",
                                       msg_text="Slack wurde für "+username+" verbunden.",
                                       userId=userId,
                                       status_text="Im Urlaub",
                                       status_emoji=":smile:")
            else:
                return render_template('tryout.html', msg_type="none",
                                       msg_text="",
                                       userId=userId,
                                       status_text="Im+Urlaub",
                                       status_emoji=":smile:")
        else:
            return render_template('install.html', error="true", error_text="(no access-token-1)")
    else:
        return render_template('install.html', error="true", error_text="(no user-id-1)")

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
            return render_template('install.html', error="true", error_text="(could not load access-token-2)")

        if (accessToken):
            # User-Profile Status setzen
            status_text = request.args.get('status_text')
            status_emoji = request.args.get('status_emoji')

            header = {
                'Authorization': 'Bearer ' + accessToken,
                'Content-type': 'application/json; charset=utf-8'
            }
            url = 'https://slack.com/api/users.profile.set'
            data = {
                "profile": {
                    "status_text": status_text,
                    "status_emoji": status_emoji
                }
            }
            r = requests.post(url=url, data=json.dumps(data), headers=header)

            ok = json.loads(r.text)['ok']
            if (ok):
                return render_template('tryout.html',
                                       msg_type="success",
                                       msg_text="Der Status wurde erfolgreich gesetzt.",
                                       userId=userId,
                                       status_text=status_text,
                                       status_emoji=status_emoji)
            else:
                return render_template('tryout.html',
                                       msg_type="danger",
                                       msg_text="Der Status konnte nicht gesetzt werden.<br>"+json.loads(r.text)['error'],
                                       userId=userId,
                                       status_text=status_text,
                                       status_emoji=status_emoji)
        else:
            return render_template('install.html', error="true", error_text="(no access-token-2)")
    else:
        return render_template('install.html', error="true", error_text="(no user-id-2)")