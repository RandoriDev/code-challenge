# John Ballentine - Randori Code Challenge

For this coding challenge, I chose to build a more robust system with a standard REST API and JSON requests.
<br /><br />
<b>1. Client Side Javascript</b><br />
   The client side encodes the user input into a JSON string, and posts it to index.html.  It uses a hidden
   form which has its value swapped by JS.  This was done to avoid using time-intensive AJAX.  On submit,
   the script submits the hidden form instead of the main form where the user selects input.
<br /><br />
<b>2. Python/Flask Service</b><br />
   The server side receives a POST request at index.html.  It first logs the request including the user IP
   address in order to check if the user has submitted the same request twice.  GET requests are also logged,
   as the requirements stated to log all requests.  IP address was chosen to identify the user as opposed to
   cookies due to both simplicity and the (slightly) better protection against denial-of-Service attacks.
   The service also validates the JSON received from the user, as well as checking if the "is_malicious"
   option is checked.  If the validation fails and/or the "is_malicious" key contains a value, execution is
   stopped and the user receives a 401: Unauthorized error.  A local SQLite database was chosen due to the
   requirement of not sending the request to the backend API unless it satisfies conditions.  The database
   logs the IP, HTTP request headers, submitted text, and timestamp.
<br /><br />
<b>3. Backend REST API</b><br />
   A serverless REST API was chosen due to the likelihood of encountering a similar setup in a real world
   working environment.  The API uses Amazon Web Service's Lambda.  API Key authentication can be implemented
   with little more than the click of a button.  However, it was not used in order to reduce the likelihood of
   complications after submission.  The service simply returns its input back to the client.
