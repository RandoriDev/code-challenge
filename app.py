from flask import Flask, render_template, request, json, abort
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
db = SQLAlchemy(app)

# Credentials for backend REST API (no authentication required)
API_URL = 'https://4rxx4pwar8.execute-api.us-east-1.amazonaws.com/live/code-challenge'


@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default.
    if request.method == 'POST':
        # JSON encode the HTML form submitted from index.html.
        received_post_json = json.dumps(request.form)
        if request.form.getlist('is_malicious') == ['is_malicious']:
            abort(401)  # Throw error: forbidden if is_malicious is flagged.
        else:
            # Ensure the MIME type is JSON in the HTTP headers.
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            api_response = requests.post(url=API_URL, data=received_post_json, headers=headers)

            # Render the API response to index.html.
            return render_template('index.html', received_post=api_response.json())
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
