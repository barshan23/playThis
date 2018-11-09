from flask import Flask,request, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import alsaaudio, os, json, vlc


option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=/home/barshan23/.config/google-chrome')
option.add_argument('--start-maximized')
timeout = 20

app = Flask(__name__)
browser = None
player = None
sound = alsaaudio.Mixer() # for controlling sound

# path to the music library
library = "/home/barshan23/Music/New/"



@app.route('/')
def index():
	return render_template('./index.html')


# route for sending youtube videos url
@app.route('/url', methods=['POST'])
def play():
	global browser
	global player
	if player:
		player.stop()
		player = None
	# if 'youtu.be' not in url:
	# 	url = url+'?v='+request.args.get('v')
	url = request.get_json()['url']
	print url
	tmode = False
	if not browser:
		tmode = True

	browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option) if not browser else browser
	browser.get(url)
	if tmode:
		# find the theater mode button
		theatre_mode = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Theater mode']")))
		print "visible"
		theatre_mode.click()
	return "playing"

# play offline song
@app.route('/url/<name>')
def play_offline(name):
	global browser
	global player
	if browser:
		browser.close()
		browser = None
	if player:
		player.stop()
		player = None
	print name
	if name:
		player = vlc.MediaPlayer(library+name)
		vlc.libvlc_audio_set_volume(player, 85)
		player.play()
	return 'playing offline'


# route for lisitng all the musics in the music library
@app.route('/musics')
def list_musics():
	musics = json.dumps([a for a in os.listdir(library) if not os.path.isdir(library+a) ])
	# print musics

	return musics


@app.route('/pp')
def play_pause():
	global browser
	if browser:
		try:
			browser.find_element_by_css_selector('button.ytp-play-button').click()
		except Exception as e:
			print e
	elif player:
		player.pause();
	return 'done'



@app.route('/fscreen')
def fscreen():
	if browser:
		try:
			browser.find_element_by_css_selector('button.ytp-fullscreen-button').click()
		except Exception as e:
			print e
	return 'done'

@app.route('/stop')
def stop():
	global browser
	global player
	if browser:
		browser.close()
		browser = None
	elif player:
		player.stop()
		player = None
	return 'Stopped'

@app.route('/vol/<number>')
def decrease(number):
	number = int(number)
	if number <= 100 and number >= 0:
		sound.setvolume(number)
	print int(sound.getvolume()[0])
	return ''

@app.route('/getvol')
def get():
	return str(int(sound.getvolume()[0]))




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)