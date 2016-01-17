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
import subprocess
import json
import datetime
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR')

# Clock Example for data update http://stackoverflow.com/questions/18923321/making-a-clock-in-kivy
# http://stackoverflow.com/questions/27213545/update-properties-of-a-kivy-widget-while-running-code
# ***** Functions *********
MBurl='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'
ForecastUpdatePeriod = 7200 # updates forecast every XX seconds
CurrentUpdatePeriod = 1800 # updates current every XX seconds


def get_daily_weather(url):
# Get daily weather info from MeteoBlue's API (all available upcoming days)
# Fetch URL, parse & return a list of DaylyData objects

  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

# Get Weather data from Json structure
	updatetime = time = datetime.datetime.now()
	daylyforecastlist = []
	for i in range(0,4):
		Dateraw = str(json.dumps(Json_decoded['forecast'][i]['date']))
		Date = Dateraw[9:11]+'-'+Dateraw[6:9]+Dateraw[1:5]
		ForecastMaxTemp = json.dumps(Json_decoded['forecast'][i]['temperature_max'])
		ForecastMinTemp = json.dumps(Json_decoded['forecast'][i]['temperature_min'])
		MaxTempColorraw = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['temperature_max_color']))
		MinTempColorraw = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['temperature_min_color']))
		MaxTempColor = list(MaxTempColorraw)
		MaxTempColor.append(1)
		MinTempColor = list(MinTempColorraw)
		MinTempColor.append(1)

		WindSpeed = json.dumps(Json_decoded['forecast'][i]['wind_speed_max'])
		WindDirraw = json.dumps(Json_decoded['forecast'][i]['wind_direction_dominant'])
		WindDir = WindDirraw[1:-1]
		WinMax = json.dumps(Json_decoded['forecast'][i]['wind_gust_max'])
		Uv = json.dumps(Json_decoded['forecast'][i]['uv_index'])
		UvColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['uv_color']))
		RainProb = json.dumps(Json_decoded['forecast'][i]['precipitation_probability'])
		RainMm = json.dumps(Json_decoded['forecast'][i]['precipitation_amount'])
		Picto = int(json.dumps(Json_decoded['forecast'][i]['pictocode_day']))
		i = DailyData(Date,ForecastMaxTemp,MaxTempColor,ForecastMinTemp,MinTempColor,WindSpeed,WindDir,WinMax,Uv,UvColor,RainProb,RainMm,Picto)
		daylyforecastlist.append(i)

	return daylyforecastlist


def get_current_weather(url):
# Get current weather info from MeteoBlue's API
# Fetch URL, parse & return a list of DaylyData objects

  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

# Get Weather data from Json structure
	updatetime = 'Mise a jour: '+ strftime("%d %b %H:%M", localtime())
	CurrentTemp = json.dumps(Json_decoded['current']['temperature'])
	Picto = int(json.dumps(Json_decoded['current']['pictocode']))
	Sunriseraw = json.dumps(Json_decoded['forecast'][0]['sunrise_time'])
	Sunsetraw = json.dumps(Json_decoded['forecast'][0]['sunset_time'])
	Pressure = json.dumps(Json_decoded['forecast'][0]['pressure_hpa'])
	Sunset = Sunsetraw[1:3]+' h '+Sunsetraw[4:6]
	Sunrise = Sunriseraw[1:3]+' h '+Sunriseraw[4:6]
	IsDaylight =  json.dumps(Json_decoded['current']['is_daylight'])
	currentweather = CurrentData(updatetime,CurrentTemp,Sunrise,Sunset,Pressure,IsDaylight, Picto)
	print('updating current')
	return currentweather




def get_weathericon(id,icontype,is_daylight):

	if icontype == 'forecast':
		if id < 10:
			iconname = './pictograms/'+'0'+str(id)+'_day.png'
		else: iconname = './pictograms/'+str(id)+'_day.png'


	if icontype == 'daily':

		if is_daylight =='1':
			daynightstring = '_iday.png'
		else: daynightstring = '_inight.png'

		if id < 10:
			iconname = './pictograms/'+'0'+str(id)+daynightstring
		else: iconname = './pictograms/'+str(id)+daynightstring

	return iconname


def hex_to_rgb(value):
  value = value.lstrip('"#')
  value = value.rstrip('"')
  #print(value)
  lv = len(value)
  #print(lv)
  return tuple(int(value[i:int(i+lv/3)], 16) for i in range(0, lv, int(lv/3)))

#***** Classes *******


class MainLayout(BoxLayout):
	pass


#****** Current weather + moon/UV Sunset info about today

class WeatherCurrent(BoxLayout):
	dayweatherlist = ListProperty(None)

	def __init__(self,currentweather='',*args,**kwargs):
		super(WeatherCurrent,self).__init__(*args,**kwargs)
		print('create WeatherCurrent')
		self.textcolor=[0.1,0.55,0.55,1]
		self.currentweather = currentweather
		Clock.schedule_once(self.update, 0.5)
		Clock.schedule_interval(self.update, CurrentUpdatePeriod)

		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
	def update(self, *args):
		self.currentweather = get_current_weather(MBurl)
		self.clear_widgets()
		self.add_widget(Label(text='Actuellement',color=self.textcolor,size_hint=[1,0.12]))
		self.add_widget(Image(source=get_weathericon(self.currentweather.Picto,'daily',self.currentweather.IsDaylight),size_hint=[1,0.4]))	
		self.add_widget(BoxLayout(size_hint=[1,0.01]))	
		self.add_widget(Label(text='Temperature : '+ str(self.currentweather.CurrentTemp)+' degres',color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Pression: '+ str(self.currentweather.Pressure)+' hPa',color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(BoxLayout(size_hint=[1,0.1]))
		self.add_widget(Label(text='Lever:  '+ str(self.currentweather.Sunrise),color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Coucher:  '+ str(self.currentweather.Sunset),color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(BoxLayout(size_hint=[1,0.1]))
		#self.add_widget(Label(text=str(self.currentweather.updatetime),color=self.textcolor))



class WeatherDay(BoxLayout):
	dayweatherlist = ListProperty(None)
	def __init__(self,dayweatherlist='',dayid='',*args,**kwargs):
		super(WeatherDay,self).__init__(*args,**kwargs)
		print('create WeatherDay')
		self.textcolor=[0.1,0.55,0.55,1]
		self.dayweatherlist = dayweatherlist
		Clock.schedule_once(self.update, 0.5)
		Clock.schedule_interval(self.update, ForecastUpdatePeriod)
		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
	def update(self, *args):
		self.dayweatherlist = get_daily_weather(MBurl)
		self.clear_widgets()
		self.add_widget(Label(text=str(self.dayweatherlist[self.dayid].Date),color=self.textcolor,size_hint=[1,0.2]))
		self.add_widget(Image(source=get_weathericon(self.dayweatherlist[self.dayid].Picto,'daily','1'),size_hint=[1,0.3]))
		self.add_widget(BoxLayout(size_hint=[1,0.1]))		
		self.add_widget(Label(text='[b]'+'Temperatures'+ '[/b]', markup=True,color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Maxi: '+ str(self.dayweatherlist[self.dayid].ForecastMaxTemp),color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Mini: '+ str(self.dayweatherlist[self.dayid].ForecastMinTemp),color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(BoxLayout(size_hint=[1,0.1]))
		self.add_widget(Label(text='[b]'+'Vent'+ '[/b]', markup=True,color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text=str(self.dayweatherlist[self.dayid].WindDir)+'   '+ str(self.dayweatherlist[self.dayid].WindSpeed)+' km/h',color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Rafales: '+ str(self.dayweatherlist[self.dayid].WindMax),color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(BoxLayout(size_hint=[1,0.1]))
		self.add_widget(Label(text='[b]'+'Pluie'+ '[/b]', markup=True,color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text=str(self.dayweatherlist[self.dayid].RainMm)+'mm, '+str(self.dayweatherlist[self.dayid].RainProb)+ '%',color=self.textcolor,size_hint=[1,0.1]))
		self.add_widget(Label(text='Indice UV: '+ str(self.dayweatherlist[self.dayid].Uv),color=self.textcolor,size_hint=[1,0.2]))




class DailyData(object):
  def __init__(self,Date, ForecastMaxTemp,MaxTempColor,ForecastMinTemp,MinTempColor,WindSpeed,WindDir,WindMax,Uv, UvColor,RainProb,RainMm,Picto):
	self.Date = Date
	self.ForecastMaxTemp = ForecastMaxTemp
	self.MaxTempColor = MaxTempColor
	self.ForecastMinTemp = ForecastMinTemp
	self.MinTempColor = MinTempColor
	self.WindSpeed = WindSpeed
	self.WindDir = WindDir
	self.WindMax = WindMax
	self.Uv = Uv
	self.UvColor = UvColor
	self.RainProb = RainProb
	self.RainMm = RainMm
	self.Picto = Picto


class CurrentData(object):
  def __init__(self,updatetime,CurrentTemp,Sunrise,Sunset,Pressure,IsDaylight, Picto):
	self.updatetime = updatetime
	self.CurrentTemp = CurrentTemp
	self.Picto = Picto
	self.Sunrise = Sunrise
	self.Sunset = Sunset
	self.Pressure = Pressure
	self.IsDaylight = IsDaylight


class KivyWeatherApp(App):

	def build(self):
		print('Program start at:', strftime("%a, %d %b %Y %H:%M:%S", localtime()))
		Window.clearcolor = (1, 1, 1, 1)
		self.mainlayout = MainLayout()
		inspector.create_inspector(Window, self.mainlayout)
		return self.mainlayout



if __name__ == "__main__":
	KivyWeatherApp().run()
