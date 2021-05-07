# Randori coding challenge submission by Eirikur Hallgrimasson, 06 May 2021

"""
    Hmmm. I thought about using redirect, which is very clean, but you want the response
    from the back end to be returned to the client. Actually, redirect just delegates that.
    I like this approach, but it doesn't handle the 2-second delay case at all well because
    you don't really have the Flask request context when the timer triggers. Maybe Flask
    was not the way to go. I hear you about scaling, so I want to use something that can
    scale. I've scaled Flask using Tornado. I'd probably study up on nginx and use that
    with a WSGI gateway in production. 

    Regrets:
       I should have written a pseudo-code design document and debugged that before coding.
       I should have used pydoc docstrings.
       I should have seen the consistency issue with the delayed case vs. immediate redirect.
       I'm definitely out of time, but you can see my thinking here, and my maintainable style.
"""

# Stdlib imports
import sys, os, syslog, logging # I like to save vertical space but this is not standard.
import logging.handlers

# Third-party imports
from flask import Flask, request, redirect # It's better than http.server because you can scale it up.
import requests



back_end_service = 'http://localhost:9000/backend' 
log_directory = os.getcwd() # There are many considerations here like log file rotation.
required_python_version = (3,5)

http_success = 200
http_invalid_endpoint = 400
http_found_redirect = 302
http_unauthorized = 401




# First things first. We must be able to report what is happening.
log = logging.getLogger(__name__) # Good practice is to not use a string here.
log.setLevel(logging.DEBUG) # Default to logging everything. 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
log.addHandler(console)

# Let's use syslog because it can be configured to log to a central logging server.
syslog = logging.handlers.SysLogHandler(address = '/dev/log')
syslog.setFormatter(formatter)
log.addHandler(syslog)

# Let's use a file because that's handy and local. TODO: support log file rotation.
fh = logging.FileHandler(f"{log_directory}{__name__}.log") # Name should be chosen intelligently :-)
fh.setLevel(logging.DEBUG)
log.addHandler(fh)




# Validate runtime environment. Add other dependency tests such as module availability.
try:
    assert sys.version_info >= required_python_version # Tuple comparisons are strange, but this is correct.
except AssertionError as e:
    log.debug(f"Python version is {sys.version_info} but this program requires {required_python_version}")
    sys.exit(1) # Exit with a bad status code so that whatever launched us knows we had a problem.



# TODO: We have no security.
app = Flask(__name__)

# It's a global dict to store requests keyed by the requesting host.
request_memory = {}

def is_a_repeated_request(rqst):
    # Is this a repeated request from the same host?
    # My first implementation expired the memory records, but that isn't
    # in the spec.
    global request_memory # Could be an object or queue, but a simple global dict will suffice.
    if rqst.host in request_memory:
        prior_request = request_memory[rqst.host]
        if prior_request.json == rqst.json:
            return True # We leave the record because we'd just replace it with identical data.
        else: # The json payload is not the same.
            prior_request.json = rqst.json # update the json
            return False
    else: # the host has no request record
        request_memory[rqst.host] = rqst # Create a record for the requesting host.
        return False

def post_to_back_end(request):
    # Action routine to POST the request to the back end.
    # This needs to magically look like the request came direct
    # from the client because I used redirect for the non-delay
    # case.
    log.info(f"POSTing request {repr(request)}")
    r = requests.post(back_end_service, data=request)
    
    
        
def delay(request):
    # Create a timer to trigger the function to send the request to the back end.
    # We don't really need a queue here.
    # Hmmm. What about returning the back end response to the client?
    # We can't assume that the client still exists.
    # So, let's get the request sent to the back end without stalling as a first pass.
    # Let the threading module handle it.    
    t = threading.Timer(2, post_to_back_end, [request])
    t.start()
    
            

def one_line(text):
    return ' '.join(str(text).split())

@app.route('/challenge', methods=['GET', 'POST'])
def challenge():
    """If the request is a POST with a json body that contains the key
    ‘is_malicious’ with the value then don’t forward the request and
    return a HTTP 401 to the client.

    If the same client makes the exact same request twice in a row
    wait 2 seconds before passing the request to the backend.

    If neither of the conditions are met then pass the request to the
    backend.

    When a request is passed on to the backend it should be forwarded
    unaltered and the backend’s response should be returned to the client.
    All processed requests should be clearly logged.

    Eirikur: The rules should impose a timeout on the 'twice in a row'
    test. I'm not doing that because I'm running out of time and need to simplify.
    I deleted a much more complex implementation of this.
    """
    
    signature = 'is_malicious'
    log.info(f"Received: {one_line(request.headers)}") # Origin info. for the log.
    json_for_log = one_line(request.json)
    if request.method == 'POST': 
        if signature not in request.json: # Let's hope this is the common case and handle it first thing.
            log.info(f"Signature |{signature}| not found in {json_for_log}")
            action = redirect(back_end_service, code=302) 
            if is_a_repeated_request(request):
                enque(request)
            else:
                return redirect(back_end_service, code=302) # Use redirect for fidelity.
        else: # The target signature was found. Something evil this way comes....
            log.info(f"ALERT: Signature |{signature}| was found in {json_for_log}")
            return '', http_unauthorized # The 401, as specified in the requirements.
                    

    else: # The request is not a POST
        return f"Sorry, but you can't {request.method} here.", http_invalid_endpoint

