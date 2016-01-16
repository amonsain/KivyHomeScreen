from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition
from KivyRadio import *
from KivyWeather import *
from ClockButton import ClockButton
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR')

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


####### MAIN

class KivyHomeScreenApp(App):

	def build(self):
		self.mainlayout = MyScreenManager()
		init_radio()
		self.mainlayout.add_widget(RadioScreen(name='RadioScreen'))
		self.mainlayout.add_widget(WeatherScreen(name='WeatherScreen'))
		inspector.create_inspector(Window, self.mainlayout)
		return self.mainlayout


if __name__ == "__main__":
	KivyHomeScreenApp().run()