import requests
import json


def send_payload(endpoint, data):
    # Convert the JSON data to a string
    json_data = json.dumps(data)

    # Set the headers to specify that you are sending JSON data
    headers = {'Content-Type': 'application/json'}

    # Send the POST request with the JSON payload
    response = requests.post(endpoint, data=json_data, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("JSON object sent successfully")
    else:
        print("Failed to send JSON object")
