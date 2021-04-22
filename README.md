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

=======================

What I completed:
- Wrote a server with the logic as requested
  - Wrote a logger middleware to log information about each processed request
- Wrote a backend server to respond to GET, POST, and PUT requests
- Wrote 21 unit tests plus 5 "integration" tests that utilize the server to make calls to the backend server

In hindsight, I should have written the is_duplicate and is_malicious logic as fastAPI middlewares. I didn't have time to do the rewrite.

Ideas of what I would add to this project if I had more time:
- Rewrite the is_duplicate and is_malicious logic as fastAPI middlewares
- Add logic to wrap the Python module in a Docker image
- Add logic to run the server and backend server as Docker containers, perhaps using Docker Compose

Time taken: Around 8 hours