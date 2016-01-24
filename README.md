# KivyHomeScreen
Interactive touch screen (Radio, Weather, ...) for Rpi, developed using python/Kivy
Kivy is multi-platfom: you can use this program on a Mac or Windows PC


Main files are:
KivyHomeScreen.py (main program) & kivyhomescreen.kv (main kivy layout file)

launch command: kivy KivyHomescreen &
"sudo kivy KivyHomescreen &" is required if you are using backlight/screensaver features on the RPi


The main program uses:
- Clockbutton.py (header button displaying Date&Time and used as a screen switcher)
- KivyWeather.py (retrieve Weather data, format current & daily forecast data, disaplay current & daily forecast weather)
- KivyRadio.py (control your local MPD/MPC player - needs to be installed & playlist needs to be defined separately)
- KivyTraffic.py (retrieve traffic data from Google DistanceMatrix API)
- backlighttoggle.py (toggles Raspberry Touchscreen backlight On/Off) (related features need to be stubbed if you are not on a Rpi with a touchscreen) 

other .kv files are used to test each menu separately 
