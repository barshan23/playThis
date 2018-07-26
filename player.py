from flask import Flask,request, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException


option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=/home/barshan23/.config/google-chrome')
option.add_argument('--start-maximized')
timeout = 20

app = Flask(__name__)
browser = None

@app.route('/')
def index():
	return render_template('./index.html')

@app.route('/url', methods=['POST'])
def play():
	global browser
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


@app.route('/pp')
def play_pause():
	if browser:
		try:
			browser.find_element_by_css_selector('button.ytp-play-button').click()
		except Exception as e:
			print e
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
	browser.close()
	browser = None
	return 'Stopped'

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)