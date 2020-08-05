# RANDORI Code Challenge - Aaron Rosano

A simple test api that runs on port 8080 and takes all methods at any single path uri (one slash)
> e.g. GET @ localhost:8080/test

## Build:
`npm install`

## Run:
`npm run start:dev`

## Test:
`npm test`


Meets criteria for code-challenge:

```
Accept HTTP requests, inspects them and then possibly pass them off to a backend service. The requirements are as follows:

If the request is a POST with a json body that contains the key ‘is_malicious’ with the value then don’t forward the request and return a HTTP 401 to the client.
If the same client makes the exact same request twice in a row wait 2 seconds before passing the request to the backend.
If neither of the conditions are met then pass the request to the backend.
When a request is passed on to the backend it should be forwarded unaltered and the backend’s response should be returned to the client.
All processed requests should be clearly logged.
```
