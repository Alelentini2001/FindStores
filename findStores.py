import webbrowser
import requests
import json
import time
import sys

#GET USER LOCATION
send_url = "http://api.ipstack.com/check?access_key=420842183c2b670d8da092c6717024f0"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

#RADAR.IO API IMPLEMENTATION
headers = {
    'Authorization': 'prj_test_sk_b5cdcfa075785c7e9712db8ef351e34bbca32c17',
}

#PLACE TO FIND CLOSE TO THE LOCATION OF THE USER
placeToFind = ""
milesRange = 0

placeToFind = input("Which place you want to find close to your location? ")
milesRange = int(input("Radius of the range in miles close to your position: "))*1000

#STORING ALL JSON RESPONSES FROM THE API
params = (
   	('query', placeToFind),
    ('near', '{},{}'.format(latitude, longitude)),
   	('radius', str(milesRange)),
    ('limit', '20'),
)

response = requests.get('https://api.radar.io/v1/search/autocomplete', headers=headers, params=params)

my_json = response.json()

#print(my_json['addresses'][0])

#CREATING A NEW DIC TO STORE ALL THE IMPORTANT THINGS INSIDE THE PREVIOUS DIC
stores = {"stores": []}
import pprint

if 'placeLabel' in my_json['addresses'][0] and my_json['addresses'][0]['placeLabel'] in placeToFind and int(my_json['addresses'][0]['distance']) < (milesRange+1):
	stores["stores"].append({"name": my_json['addresses'][0]['placeLabel'],"address": my_json['addresses'][0]['formattedAddress'], "distance": (str(round(float((my_json['addresses'][0]['distance'])*0.000621),2))+" miles"), "latitude": my_json['addresses'][0]['latitude'], "longitude": my_json['addresses'][0]["longitude"], "link": "https://www.google.com/maps/search/?api=1&query={},{}".format(my_json['addresses'][0]['latitude'],my_json['addresses'][0]['longitude'])})
if len(my_json['addresses']) > 1:
	for j in range(0, len(my_json['addresses'])):
		if 'placeLabel' in my_json['addresses'][j] and my_json['addresses'][j]['placeLabel'] in placeToFind and int(my_json['addresses'][j]['distance']) < (milesRange+1):
			if my_json['addresses'][j]['formattedAddress'] not in stores["stores"]:
				stores["stores"].append({"name": my_json['addresses'][j]['placeLabel'],"address": my_json['addresses'][j]['formattedAddress'], "distance": (str(round(float((my_json['addresses'][j]['distance'])*0.000621),2))+" miles"), "latitude": my_json['addresses'][j]['latitude'], "longitude": my_json['addresses'][j]["longitude"], "link": "https://www.google.com/maps/search/?api=1&query={},{}".format(my_json['addresses'][j]['latitude'],my_json['addresses'][j]['longitude'])})
#pprint.pprint(stores["stores"])
#print(stores['stores'][0])

for i in range(0, len(stores['stores'])):
	print(f"{i} - {stores['stores'][i]['name']}\n  {stores['stores'][i]['address']}\n  {stores['stores'][i]['distance']}\n  {stores['stores'][i]['latitude']},{stores['stores'][i]['longitude']}\n  {stores['stores'][i]['link']}")


if(len(stores['stores']) != 0):
	print()
	openLink = int(input(f"Which link you want to open (from 0 to {len(stores['stores'])-1}): "))
	print()
	linkToOpen = stores['stores'][openLink]['link']
else: 
	print(f"No {placeToFind} near your range\n")
	exit()

#https://www.google.com/maps/search/?api=1&query=51.3905399,-0.5067432

toolbar_width = 40

# setup toolbar
sys.stdout.write(f"Opening the link [%s]" % ("-" * toolbar_width))
sys.stdout.flush()
sys.stdout.write(f"\b" * (toolbar_width+1)) # return to start of line, after '['

for i in range(toolbar_width):
    time.sleep(0.2) # do real work here
    # update the bar
    sys.stdout.write("#")
    sys.stdout.flush()

sys.stdout.write(f"]\nOpening!\n") # this ends the progress bar

webbrowser.open(linkToOpen)