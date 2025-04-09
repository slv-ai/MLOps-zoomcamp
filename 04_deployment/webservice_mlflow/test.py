import requests
ride={
    "PULocationID" : 10,
    "DOLocationID" : 50,
    "trip_distance" : 40
}
url='http://localhost:9696/predict'
response=requests.post(url,json=ride)
if response.status_code == 200:
    try:
        print(response.json())  # Only attempt to parse JSON if the response is valid
    except ValueError:
        print("Response content is not valid JSON.")
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response content:", response.text)
#print(response.json())