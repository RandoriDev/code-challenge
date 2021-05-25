from flask import Flask, render_template, request, json, abort
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
db = SQLAlchemy(app)

# Credentials for backend REST API (no authentication required)
API_URL = 'https://4rxx4pwar8.execute-api.us-east-1.amazonaws.com/live/code-challenge'


@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'POST':
        # Get the element from the hidden form that contains the JSON string from the main form
        post_received_json = request.form['json_element']
        # Get a dict from the
        post_received_dict = json.loads(post_received_json)

        if post_received_dict['is_malicious'] == 'is_malicious':
            abort(401)
        else:
            api_post = requests.post(url=API_URL, data=post_received_json)
            return render_template('index.html', received_post=json.dumps(post_received_dict))         #api_post.json())
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
