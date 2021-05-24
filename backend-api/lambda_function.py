import json


def lambda_handler(event, context):

    # Store posted text from query in variable
    post_text = event['post_text']

    # Build response object
    response = []
    response['post_text'] = post_text

    # Build the HTTP response object from the response object
    response_http = []
    response_http['statusCode'] = 200
    response_http['headers'] = {}
    response_http['headers']['Content-Type'] = 'application/json'
    response_http['body'] = json.dumps(post_text)

    return response_http
