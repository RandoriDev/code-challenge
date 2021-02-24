# Code Challenge

## Problem Statement
Build a service that accepts HTTP requests, inspects  and possibly pass to a backend service.

### Requirements
- If the request is a POST with a json body that contains the key ‘is_malicious’ with the value then don’t forward the request and return a HTTP 401 to the client.
- If the same client makes the exact same request twice in a row wait 2 seconds before passing the request to the backend.
- If neither of the conditions are met then pass the request to the backend.
- When a request is passed on to the backend it should be forwarded unaltered and the backend’s response should be returned to the client.
- All processed requests should be clearly logged.

## Submission

### Assumptions
- No authentication is necessary for this exercise
- Each request is stateless
- backend service is not accessible directly except to httpservice

### Implementation Notes
Implementation is in Python

Web Framework - Flask

httpservice acts as forwarding proxy. It takes care of
- Serving errors
- Validating requests
- Throttling requests

backendservice would do the meat of the work


### Directory Structure
+--- httpservice

|     +--- app

|     +--- service

|     +--- tests

+--- backend

|     +--- app

|     +--- service

|     +--- tests

app -> Flask specific code

service -> Service specific code

tests -> pytest based tests

### Running the service
I did the exercise on a windows machine, please adjust instructions for Mac, Linux as appropriate. Source code in my case was in the folder `s:\randori\simple-V2\`. Python virtual env is created in the folder `s:\venv\randori\`

- Download source code in the PR
- Create a python virtual env 
`python -m venv s:\venv\randori`
- Activate the virtual env
`s:\venv\randori\activate.bat`
- Set PYTHONPATH 
`set PYTHONPATH=s:\randori\simple-V2\`
This is necessary to ensure all the includes work correctly
- Navigate to the source code folder and install the necessary modules
```
cd s:\randori\simple-V2\httpservice
pip install requirements.txt
```
- Run httpservice
```
cd s:\randori\simple-V2\httpservice
python app\main.py
```
- Run backend service
```
cd s:\randori\simple-V2\backend
pip install requirements.txt
python app\main.py
```
This allows to run the two services locally using Flask. For production env use gunicorn / uWSGI container or for hosted options use a provider like Google App Engine / Azure / Heroku. gunicorn / uWSGI allow multi threading for scale.

To do a simple test on the service 
```
cd s:\randori\simple-V2\
set PYTHONPATH=s:\randori\simple-V2\
python client.py
```

It should show the output
```
{
  "message": "Processed by the backend service!"
}
```


### Logging
app.log files are produced for each service in their base folder. E.g. httpservice\app.log, backend\app.log

### Testability
Unit tests can be run on each service

#### test backend
```
set PYTHONPATH=s:\randori\simple-V2\
cd s:\randori\simple-V2\backend
pytest
```

#### test httpservice

httpservice depends on backend service. Start backend service prior to testing the httpservice

Start the backend service
```
set PYTHONPATH=s:\randori\simple-V2\
cd s:\randori\simple-V2\backend
python app\main.py
```
test httpservice
```
set PYTHONPATH=s:\randori\simple-V2\
cd s:\randori\simple-V2\httpservice
pytest
```

client.py has a simple client to exercise the functionality

### Potential Improvements
- The problem statement as described is a synchronous implementation in python. This is appropriate for some use cases like serving UI. For use cases like processing data collected by a client, we can look in to asynchronous processing providing better scale.
- Containerize the two services or host them on a public provider like Google App Engine / Azure / Heroku
- Logs should go to a common log provider
- GOLANG is a better choice for implementing the forwarding proxy than Python