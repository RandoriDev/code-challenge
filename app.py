from flask import Flask, render_template, request, json, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests, traceback

app = Flask(__name__)

# Request Log Database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/logs.sqlite'
db = SQLAlchemy(app)


class LogRequest(db.Model):
    __tablename__ = 'request_log'
    id = db.Column(db.Integer, primary_key=True)
    request_method = db.Column(db.String)
    request_headers = db.Column(db.Text)
    request_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Credentials for backend REST API (no authentication required)
API_URL = 'https://4rxx4pwar8.execute-api.us-east-1.amazonaws.com/live/code-challenge'


# Have exceptions return 401: Unauthorized
@app.errorhandler(Exception)
def unauthorized_abort(e):
    abort_string = "<h1>401: UNAUTHORIZED</h1>" \
                 + "<p>The request has not been applied because it lacks<br>" \
                 + "valid authentication credentials for the target resource.</p>"
    return abort_string, 401


app.register_error_handler(401, unauthorized_abort)


@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'GET':  # Log GET requests as well as POST requests
        # Build request data for log entry
        log_entry_headers = str(request.headers)

        request_log = LogRequest(request_method='GET', request_headers=log_entry_headers, request_text="")
        db.session.add(request_log)
        db.session.commit()

        return render_template('index.html')

    elif request.method == 'POST':
        log_entry_headers = str(request.headers)
        # Get the element from the hidden form that contains the JSON string from the main form
        post_received_json = request.form['json_element']

        request_log = LogRequest(request_method='POST', request_headers=log_entry_headers, request_text=post_received_json)
        db.session.add(request_log)
        db.session.commit()

        # Convert JSON to dict
        post_received_dict = json.loads(post_received_json)

        # Validate JSON and make sure the received request is JSON-encoded.
        json.loads(request.form['json_element'])

        # Check if is_malicious is flagged and throw an exception if so.
        if post_received_dict['is_malicious'] == 'is_malicious':
            raise Exception
        else:
            api_post = requests.post(url=API_URL, data=post_received_json)
            return render_template('index.html', received_post=api_post.json())
    else:
        raise Exception


if __name__ == '__main__':
    app.run()
