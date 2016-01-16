from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from time import gmtime, strftime, localtime
import locale
from string import capitalize

locale.setlocale(locale.LC_ALL, 'fr_FR')

class ClockButton(Button):

	def __init__(self,*args,**kwargs):
		super(ClockButton,self).__init__(*args,**kwargs)
		Clock.schedule_interval(self.update, 15)

	def update(self, *args):
		self.text = strftime("%A %d %B %H:%M", localtime()).capitalize()
		self.font_size = 40
		self.markup=True
		self.color = [1,1,1,1]
		self.background_color=[0.1,0.55,0.55,1]
		print(self.text)
