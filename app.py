from flask import Flask, render_template, request, json, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests, time

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
    ip_address = db.Column(db.String)
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
def index():
    if request.method == 'GET':  # Log GET requests.

        # Build request data for log entry
        log_entry_headers = str(request.headers)

        request_log = LogRequest(request_method='GET', request_headers=log_entry_headers, request_text="",
                                 ip_address=request.remote_addr)
        db.session.add(request_log)
        db.session.commit()

        return render_template('index.html')

    elif request.method == 'POST':  # Log POST requests.
        log_entry_headers = str(request.headers)

        # Get the element from the hidden form that contains the JSON string from the main form
        post_received_json = request.form['json_element']

        # Validate JSON and make sure the received request is JSON-encoded.
        # Will throw an exception if fails, and cause a 401: Unauthorized response.
        json.loads(request.form['json_element'])

        request_log = LogRequest(request_method='POST', request_headers=log_entry_headers,
                                 request_text=post_received_json, ip_address=request.remote_addr)

        # Check by IP address if user posted the same request twice.
        query_result = request_log.query.filter_by(ip_address=request.remote_addr,
                                                   request_method='POST').order_by(LogRequest.id.desc()).first()
        if query_result:
            if query_result.request_text == post_received_json:
                time.sleep(2)

        # Add the database entry after the check.
        db.session.add(request_log)
        db.session.commit()

        # Convert JSON to dict
        post_received_dict = json.loads(post_received_json)

        # Check if is_malicious is flagged and throw an exception if so.
        if post_received_dict['is_malicious'] == 'is_malicious':
            raise Exception
        else:
            # Get only text_field from the JSON response.
            api_response = requests.post(url=API_URL, data=post_received_json)
            api_response_split = json.loads(api_response.text)
            api_response_dict = json.loads(api_response_split['body'])
            return render_template('index.html', api_response=api_response_dict['text_field']) #api_response_dict['text_field'])
    else:
        raise Exception


if __name__ == '__main__':
    app.run()
