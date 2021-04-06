randori-context
=======

randori bounded context


steps to install randori
===

```

1. Unzip project

#Create virtualEnv
2. python3.6 -m venv randori

3. cd randori

4. source bin/activate

5. pip install -r requirements.txt

6. python -m rest.app

```

===
#To execute in production use gunicorn or other cgi server

#Call this url to test the endpoint to test get and post
#http://localhost:3001/apiGateway?url=http://localhost:3001/dummy
