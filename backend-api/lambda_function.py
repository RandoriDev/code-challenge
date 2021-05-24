# A REST API Designed to run on Amazon Lambda.
# The API is POSTed to with a JSON object containing a single value:
# post_text.  It then returns that value in JSON format.

import json


def lambda_handler(event, context):

    # Store posted text from query in variable
    post_text = event['post_text']

    # Build response object
    response = {'post_text': post_text}

    # Build the HTTP response object from the response object
    response_http = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(post_text)
    }

    return response_http
