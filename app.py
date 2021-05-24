from flask import Flask, render_template, request, json, abort
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
db = SQLAlchemy(app)

# Credentials for backend REST API (no authentication required)
API_URL = 'https://5fr2ve0kda.execute-api.us-east-1.amazonaws.com/production/code-challenge-api/'


@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'POST':
        post_received_json = json.dumps(request.form)
        if request.form.getlist('is_malicious') == ['is_malicious']:
            abort(401)
        else:
            api_post = requests.post(url=API_URL, json=post_received_json)
            return render_template('index.html', received_post=post_received_json)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
