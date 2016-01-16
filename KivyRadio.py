from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
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
import subprocess



# ***** Functions *********

def toggle_radio(state,channel):
	print('toggle radio ' + str(state) + ' ' + str(channel))
	if state =='normal':
		#subprocess.check_output(["mpc","stop"])
		print('extinction radio')
	else:
		#subprocess.check_output(["mpc","play",str(channel)])
		print('allumage canal: ' + str(channel))

def change_volume(level):
	print('Change volume' + str(level))
	volume_input = level
	if volume_input==0:
		compensated_volume=0
	else: compensated_volume=70+volume_input*30/100
	#subprocess.check_output(["mpc","volume",str(compensated_volume)])


def init_radio():
	#subprocess.check_output(["mpc","clear"])
	#subprocess.check_output(["mpc","load","kivyplaylist"])
	#subprocess.check_output(["mpc","volume",str(75)])
	pass

# ***** Classes *******

class MainLayout(BoxLayout):
	pass

class VolumeSlider(Slider):
	def __init__(self,*args,**kwargs):
		super(VolumeSlider,self).__init__(*args,**kwargs)
		self.value=25
		print(self.value)
		self.bind(value=self.update_value)

	def update_value(self,*args):
		change_volume(int(self.value))


class RadioButton(ToggleButton):
	#icon = StringProperty(None)
	def __init__(self,stationid='',stationname='',textcolor='',*args,**kwargs):
		super(RadioButton,self).__init__(*args,**kwargs)
		self.stationid = stationid
		self.stationname = stationname
		self.textcolor = textcolor
		self.group='Station'
		with self.canvas.after:
			self.radiobox = BoxLayout(orientation='horizontal')
			self.radiobuttonlabel = Label(font_size=60,size_hint=[0.8,1],markup=True,color=self.textcolor)
			self.radiobuttonimage = Image(source='./images/playbuttonwhite.png',size_hint=[0.2,1])			
			self.radiobox.add_widget(self.radiobuttonlabel)
			self.radiobox.add_widget(self.radiobuttonimage)	
			self.add_widget(self.radiobox)
			self.background_normal = ''
			self.background_down = ''

		self.bind(pos=self.update_radiobox,size=self.update_radiobox)
		self.bind(state=self.update_state)

	def update_radiobox(self,*args):
		self.radiobox.pos = self.pos
		self.radiobox.size = self.size
		self.radiobuttonlabel.text = '[b]'+str(self.stationname)+'[/b]'
		self.radiobuttonlabel.color = self.textcolor
		self.background_color =[0.7,0.7,0.7,1]		



	def update_state(self,*args):
		print('update state')
		if self.state == 'normal':
			self.radiobuttonimage.source = './images/playbuttonwhite.png'
		else: self.radiobuttonimage.source  = './images/whitepause.png'

	def on_press(self):
		print('press Station ' + str(self.stationid))
		toggle_radio(self.state,self.stationid)



class KivyRadioApp(App):
	source = StringProperty()
	def build(self):
		mainlayout = MainLayout()
		init_radio()
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyRadioApp().run()