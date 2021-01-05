# code-challenge
Software Developer Coding Challenge

Our goal is to better understand you as an engineer and not proficiency in any one specific language.  Please work in the language you are most comfortable so we can best understand how you work.  We need to make sure we can properly review the project so please stick to Python, Go, Java, C, C++, Javascript or Rust.  If your favorite language isn’t on the list, let us know and we can talk about it.

We would like you to build a service that will accept HTTP requests, inspects them and then possibly pass them off to a backend service.  The requirements are as follows:

1.  If the request is a POST with a json body that contains the key ‘is_malicious’ with the value then don’t forward the request and return a HTTP 401 to the client.
2.  If the same client makes the exact same request twice in a row wait 2 seconds before passing the request to the backend.
3.  If neither of the conditions are met then pass the request to the backend.
4.  When a request is passed on to the backend it should be forwarded unaltered and the backend’s response should be returned to the client.  
5.  All processed requests should be clearly logged.

At Randori we value core software engineering principles and we are looking more for that than just a high performance solution.  We favor a maintainable, testable implementation with clear documentation.  Don’t be afraid to reach out if anything in the requirements doesn’t make sense;  We are happy to clarify any questions you have.    This assignment should ideally should take no more than 4-6 hours.

## Configuration
The proxy can currently be configured via the following options:
|Env Var|CLI Param|Description|Default|
|-|-|-|-|
|`LISTEN_ADDR`|`--listen-addr`|Sets the address of the proxy's backend|`127.0.0.1:8080`|
|`BACKEND_URL`|`--backend-url`|Sets the URL of the proxy's backend|`http://127.0.0.1:8081`|
||`--help`|Displays help||
## To Run 

### Via Docker
```
docker build -t randori-code-challenge:v1 ./
docker run -p 8080:8080 \
  -e LISTEN_ADDR=0.0.0.0:8080 \
  -e BACKEND_URL=http://my-backend-server \
  randori-code-challenge:v1
```
### Via Go
```
go build -o proxy
./proxy --backend-url=http://127.0.0.1:8081
```

## To Test
```
docker build -t randori-code-challenge:test --target dev ./
docker run randori-code-challenge:test
```

## Captured Output

### Proxy Logs
```
2021/01/04 20:24:39 Starting proxy server
2021/01/04 20:24:39 Listening on 127.0.0.1:8080
2021/01/04 20:24:39 Forwarding to http://127.0.0.1:8081
2021/01/04 20:24:44 127.0.0.1:56714 - ["GET /foo/bar" curl/7.58.0] 15 false [200]
2021/01/04 20:24:48 127.0.0.1:56722 - ["GET /foo/bar" curl/7.58.0] 2000280 true [200]
2021/01/04 20:24:50 127.0.0.1:56724 - ["GET /foo" curl/7.58.0] 10 false [200]
2021/01/04 20:25:30 127.0.0.1:56726 - ["POST /api/login" curl/7.58.0] 0 false [401]
2021/01/04 20:25:30 [WARN] Malicious activity detected from 127.0.0.1:56726
```

### Test Logs
```
=== RUN   TestProxyRecorder
--- PASS: TestProxyRecorder (0.00s)
=== RUN   TestProxyBasic
2021/01/04 20:26:46 127.0.0.1:59562 - ["GET /" Go-http-client/1.1] 63 false [200]
--- PASS: TestProxyBasic (0.00s)
=== RUN   TestProxyMalicious
2021/01/04 20:26:46 127.0.0.1:58784 - ["POST /" Go-http-client/1.1] 0 false [401]
2021/01/04 20:26:46 [WARN] Malicious activity detected from 127.0.0.1:58784
--- PASS: TestProxyMalicious (0.00s)
=== RUN   TestProxyDuplicate
2021/01/04 20:26:46 127.0.0.1:42264 - ["GET /" Go-http-client/1.1] 12 false [200]
2021/01/04 20:26:48 127.0.0.1:42268 - ["GET /" Go-http-client/1.1] 2000266 true [200]
2021/01/04 20:26:48 127.0.0.1:42270 - ["GET /" Go-http-client/1.1] 13 false [200]
--- PASS: TestProxyDuplicate (2.00s)
PASS
ok      github.com/RandoriDev/code-challenge/pkg/proxy  2.010s
```
