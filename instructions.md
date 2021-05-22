
## MiddleWare Layer

The layer was built using python, pytest and tavern.


### Deploy

* Install the required dependencies
```
pip install -r requirements.txt
```

* Run service
```
python ./middleware.py &
```
* Run tests
```
pytest
```

### Usage

Endpoint doesn't forward the request and returns a HTTP 401 to the client
```
curl -XPOST http://127.0.0.1:8000 -d '{"is_malicious": 1}'
```

Endpoint forwards request unaltered and the backend's response returns to the client
```
curl -XGET http://127.0.0.1:8000
curl -XPOST http://127.0.0.1:8000
curl -XPOST http://127.0.0.1:8000 -d '{"foo": 'bar"}'
```
