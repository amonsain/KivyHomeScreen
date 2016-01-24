from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.modules import inspector
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from time import gmtime, strftime, localtime
import urllib
import json

GMAPIkey = 'AIzaSyAC24-Uuz1Fo04Q3J6gjrJU_v86PPEYFJ0'

GMAPURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?mode=driving&'

TrafficUpdatePeriod = 900 # updates Traffic every XX seconds

def get_transittime(start,destination):
	transittime =[]
	url = GMAPURL + 'origins='+start+'&destinations='+destination+'&key='+GMAPIkey+'&departure_time=now'
	print url
	try:

		gmaps_api_reply = urllib.urlopen(url)
		Json_string = gmaps_api_reply.read().decode('utf-8')
		Json_decoded = json.loads(Json_string)

		duration = json.dumps(Json_decoded['rows'][0]['elements'][0]['duration']['text'])
		duration_traffic = json.dumps(Json_decoded['rows'][0]['elements'][0]['duration_in_traffic']['text'])
		distance = json.dumps(Json_decoded['rows'][0]['elements'][0]['distance']['text'])
		duration_inseconds = float(int(json.dumps(Json_decoded['rows'][0]['elements'][0]['duration']['value'])))
		duration_traffic_inseconds = int(json.dumps(Json_decoded['rows'][0]['elements'][0]['duration_in_traffic']['value']))
		trafficratio = duration_traffic_inseconds / duration_inseconds
		if trafficratio < 1.1:
			traffic_state = 'low'
		elif trafficratio > 1.6:
			traffic_state = 'high'
		else: trafficratio = 'med'

		transittime.append(duration)
		transittime.append(duration_traffic)
		transittime.append(distance)
		transittime.append(traffic_state)

	except ValueError:
		print('Could not get traffic data from Google API')

	return transittime


class MainLayout(BoxLayout):
	pass


class TrafficCurrent(BoxLayout):

	def __init__(self,start='',destination='',*args,**kwargs):
		super(TrafficCurrent,self).__init__(*args,**kwargs)
		print('create Traffic Current')
		self.textcolor=[0.1,0.55,0.55,1]
		
		# force widget update right after creation & schedule updates according to TrafficUpdatePeriod
		Clock.schedule_once(self.update, 0.5)
		Clock.schedule_interval(self.update, TrafficUpdatePeriod)

		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
	
	def update(self, *args):
		self.traffic = get_transittime(self.start,self.destination)
		self.clear_widgets()
		#print('updating Traffic info')

		traffic_icon = './images/'+self.cartype +'-'+self.traffic[3]+'.png'
		#print traffic_icon

		# Display Traffic info & pictogram 
		self.add_widget(Label(text=self.nom,color=self.textcolor,size_hint=[1,0.12],font_size='25sp'))
		self.add_widget(Label(text='Duree de trajet: '+ self.traffic[1][1:-1],color=self.textcolor,size_hint=[1,0.12],font_size='25sp'))
		self.add_widget(Label(text='Distance: '+ self.traffic[2][1:-1],color=self.textcolor,size_hint=[1,0.12],font_size='25sp'))
		self.add_widget(Image(source=traffic_icon,size_hint=[1,0.12]))



class KivyTrafficApp(App):

	def build(self):
		print('Traffic start at:', strftime("%a, %d %b %Y %H:%M:%S", localtime()))
		Window.clearcolor = (1, 1, 1, 1)
		self.mainlayout = MainLayout()
		inspector.create_inspector(Window, self.mainlayout)
		return self.mainlayout



if __name__ == "__main__":
	KivyTrafficApp().run()
