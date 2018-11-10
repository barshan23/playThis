from flask import Flask,request, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains # this is used to do the mouse over
import alsaaudio, os, json, vlc, time


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
	duration = browser.find_element_by_css_selector('span.ytp-time-duration').text
	current = browser.find_element_by_css_selector('span.ytp-time-current').text
	return json.dumps({'done' : True, 'offline': False, 'duration' : duration, 'current' : current})

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
	return json.dumps({'done' : True, 'offline' : True})


# route for lisitng all the musics in the music library
@app.route('/musics')
def list_musics():
	musics = json.dumps([a for a in os.listdir(library) if not os.path.isdir(library+a)])
	return musics


@app.route('/pp')
def play_pause():
	global browser
	# print player
	if browser:
		print "browser"
		try:
			browser.find_element_by_css_selector('button.ytp-play-button').click()
		except Exception as e:
			print e
		return json.dumps({'done' : True})

	elif player:
		player.pause();
		return json.dumps({'done' : True})
	return json.dumps({'done' : False})
	


@app.route('/fscreen')
def fscreen():
	if browser:
		try:
			browser.find_element_by_css_selector('button.ytp-fullscreen-button').click()
		except Exception as e:
			print e
		return json.dumps({'done' : True})
	return json.dumps({'done' : False})

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



@app.route('/position')
def get_position():
	if player:
		pos = player.get_position();
		return json.dumps({'pos' : pos, 'offline' : True})
	elif browser:
		while True:
			try:
				# first do a mouse hover over the video player to get the current time
				ActionChains(browser).move_to_element(browser.find_element_by_css_selector('span.ytp-time-current')).perform()
				time.sleep(1)
				current = browser.find_element_by_css_selector('span.ytp-time-current').text.split(':')
			except Exception as e:
				print e
				return json.dumps({'pos' : False})
			print current
			if len(current) >= 2:
				break
		# print browser.find_element_by_css_selector('span.ytp-time-current').text
		print current
		current = [int(a) for a in current] if len(current) == 3 else [0,int(current[0]), int(current[1])]
		print current
		return json.dumps({'offline' : False, 'pos' : current})
	return json.dumps({'pos' : False})


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)