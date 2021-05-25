# A REST API Designed to run on Amazon Lambda.
# The API is POSTed to with a JSON object containing a single value:
# post_text.  It then returns that value in JSON format.

import json


def lambda_handler(event, context):

    print(event)

    # Store posted text from query in variable
    text_field = event['text_field']

    # Build response object
    response = {'text_field': text_field}

    # Build the HTTP response object from the response object
    response_http = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }

    return response_http
