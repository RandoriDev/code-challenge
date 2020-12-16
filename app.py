from flask import Flask, jsonify, request

from core import backend
from core.decorators.decorators import reject_malicious_payload, rate_limited

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
@reject_malicious_payload
@rate_limited
def index():
    """
    When a request is passed on to the backend it should be forwarded unaltered
    and the backend’s response should be returned to the client.
    """

    message = backend.handle_request(unaltered_request=request)
    return jsonify({"message": message}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)