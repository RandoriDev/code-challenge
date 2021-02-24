import requests

# Call httpservice with basic params
r = requests.post("http://127.0.0.1/", json={ "foo": "bar"})

# Call httpservice with is_malicious
#r = requests.post("http://127.0.0.1/", json={ "foo": "bar", "is_malicious" : "test"})

print(r.text) # displays the result body.
