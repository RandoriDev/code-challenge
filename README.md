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

--------------------------------------------------------------------

Randori Code Challenge using GoLang.

In Order to Run:
    - Open two Visaul Studio Code Instances, one at the root, one in the "fake_endpoint" folder.
    - run the "fake_endpoint/endpoint.go" file
    - run the "main.go" file in the root
    - using curl or postman, you can now send POST commands with JSON bodies.
    - If you want to see it working on a real api, modify the "main.go" URL and re-run "main". You won't need the "fake_endpoint" at that point

Tests:
    - There is a file "http_test.go" that you can run tests on, it requires the "fake_endpoint", and "main.go" files to be in their original state (i.e. Looking at Localhost)
    - just run "go test http_test.go"
