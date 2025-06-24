from flask import Flask, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = "2883439835182858"
CLIENT_SECRET = os.getenv("META_CLIENT_SECRET")
REDIRECT_URI = "https://meta-webhook-to-make.onrender.com/oauth/callback"

@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "❌ Code manquant dans l'URL.", 400

    # Appel pour échanger le code contre un access_token
    token_url = f"https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    res = requests.get(token_url, params=params)
    if res.status_code != 200:
        return f"❌ Erreur lors de l'échange du code :<br><br>{res.text}", 400

    access_token = res.json().get("access_token")
    return f"""
        ✅ <strong>Connexion réussie !</strong><br><br>
        Voici ton token, copie-le et envoie-le à Adrien :<br><br>
        <textarea style='width:90%; height:150px'>{access_token}</textarea>
    """

@app.route('/')
def index():
    return '✅ Webhook Meta → Make opérationnel.'

if __name__ == '__main__':
    app.run(debug=True)
