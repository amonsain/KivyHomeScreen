import googlemaps


GMAPIkey = 'AIzaSyAC24-Uuz1Fo04Q3J6gjrJU_v86PPEYFJ0'

def get_transittime(start,destination):

https://maps.googleapis.com/maps/api/directions/json?origin=Colomiers&destination=Lacroix-Falgarde&mode=driving&traffic_model=optimistic&departure_time=now

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

	
	client = googlemaps.Client(GMAPIkey)
	transittime = client.directions(start,destination, mode="driving")
	return transittime