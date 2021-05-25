from flask import Flask, render_template, request, json, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

# Request Log Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/logs.sqlite'
db = SQLAlchemy(app)


class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_text = db.Column(db.Text, unique=True, nullable=False)
    ip_address = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, request_text, ip_address, timestamp):
        self.request_text = request_text
        self.ip_address = ip_address
        self.timestamp = timestamp

    def __repr__(self):
        return "(Request Text: %s, IP Address: %s, Timestamp: %s)" \
               % (self.request_text, self.ip_address, self.timestamp)

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
            return render_template('index.html', received_post=api_post.json())
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
