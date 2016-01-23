from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition
from KivyRadio import *
from KivyWeather import *
from KivyTraffic import *
from ClockButton import ClockButton
import locale
import subprocess
from backlighttoggle import set_backlight

locale.setlocale(locale.LC_ALL, 'fr_FR')

def on_motion(self, etype, motionevent):
	screensavermanager(self)
	print(etype)
	pass

def screensavermanager(self,*args):
	set_backlight('on')
	Clock.unschedule(turnscreenoff)
	print('unschedule previous turn-off')
	Clock.schedule_once(turnscreenoff,300)
	print('Turn screen on and schedule screen turn shutdown')

def turnscreenoff(self,*args):
	set_backlight('off')
	print('Screen turns off')


class MyScreenManager(ScreenManager):

	def delayedswitch(self):
		Clock.schedule_once(self.switchtoweather,30)
		print('schedule switch back to Weather screen in 30 sec.')

	def switchtoweather(self,*args):

		self.current = 'WeatherScreen'

class RadioScreen(Screen):
	pass

class WeatherScreen(Screen):
	pass

class TrafficScreen(Screen):
	pass

####### MAIN

class KivyHomeScreenApp(App):

	def build(self):
		self.mainlayout = MyScreenManager()
		init_radio()
		self.mainlayout.add_widget(RadioScreen(name='RadioScreen'))
		self.mainlayout.add_widget(WeatherScreen(name='WeatherScreen'))
		self.mainlayout.add_widget(TrafficScreen(name='TrafficScreen'))		
		inspector.create_inspector(Window, self.mainlayout)
		Window.bind(on_motion=on_motion)
		return self.mainlayout

if __name__ == "__main__":
	KivyHomeScreenApp().run()