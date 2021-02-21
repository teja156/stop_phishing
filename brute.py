import requests
import proxyassist
import random
import sys
import string
import logging
import os
import time
import discord_webhook
import threading
import schedule
from pytz import timezone
from datetime import datetime 

URL = "http://copyrightform-helpcenter.tk/support/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}


USE_PROXY = sys.argv[1]
SUBMITTED_COUNT = 0

tz = timezone('Asia/Kolkata')
def timetz(*args):
    return datetime.now(tz).timetuple()

logging.Formatter.converter = timetz
logging.basicConfig(filename="logs.log", format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG) 


def submitForm(ip):
	global SUBMITTED_COUNT
	ip_port = ip

	if ip_port!="0":
		print("Using %s"%ip_port)
		logger.debug("Using %s"%ip_port)

	proxyDict = {"http":ip_port,"https":ip_port}

	s = requests.Session()
	uname_size = random.randint(5,10)
	uname = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = uname_size))
	passwd_size = random.randint(8,20)
	passwd = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = uname_size))
	data = {'password':passwd}

	if ip_port == "0":
		# No proxy
		try:
			r = s.get(URL + "login.php?nick=%s"%(uname),headers=headers)
			r = s.post(URL + "login.php?nick=%s"%(uname),headers=headers,data=data)
			r = s.post(URL + "confirmed.php?",headers=headers)
		except Exception as e:
			# IP blocked or site is down
			print("Connection failed with no proxy")
			logger.error("Error - %s"%e)
			discord_webhook.send_msg(status='error',sent=SUBMITTED_COUNT,error="Connection with real IP failed - %s"%e)
			return 0


	else:
		# Use Proxy
		try:
			r = s.get(URL + "login.php?nick=%s"%(uname),headers=headers,proxies=proxyDict)
			r = s.post(URL + "login.php?nick=%s"%(uname),headers=headers,proxies=proxyDict,data=data)
			r = s.post(URL + "confirmed.php?",headers=headers,proxies=proxyDict)
		except Exception as e:
			print("Error - ",e)
			logger.error("Error - %s"%e)
			discord_webhook.send_msg(status='error',sent=SUBMITTED_COUNT,error="Proxy IP connection failed - %s"%e)
			return 0


	if r.status_code!=200:
		return 0

	if "We apologize for the problem you encountered" in r.text:
		print("Sent %s, %s successfully!"%(uname,passwd))
		SUBMITTED_COUNT+=1
		logger.info("Submitted %s, %s - %d"%(uname,passwd,SUBMITTED_COUNT))
		
		if SUBMITTED_COUNT%50==0:
			logger.info("SUBMITTED UNTIL NOW - %d"%SUBMITTED_COUNT)

	return 1


def discord_notify():
	global SUBMITTED_COUNT
	discord_webhook.send_msg(status='info',sent=SUBMITTED_COUNT,error="")

def sched_discord_notify():
	schedule.every().hour.do(discord_notify)
	# schedule.every(20).seconds.do(discord_notify)
	while 1:
		schedule.run_pending()
		time.sleep(1)

def start():
	thr = threading.Thread(target=sched_discord_notify,args=(),daemon=True)
	thr.start()
	ip = "0"

	print("USE_PROXY = %s"%USE_PROXY)

	if USE_PROXY == "1":
		ip = proxyassist.getProxyAddress()

	while 1:
		if not(ip):
			print("No Proxy addresses were valid!")
			ip = "0" # Use no proxy

		if submitForm(ip)==0:
			if USE_PROXY == "1":
				# IP FAIL, get another IP
				print("Trying to find a proxy..")
				ip = proxyassist.getProxyAddress()
			if USE_PROXY == "0":
				print("Real IP BLOCKED or the SITE IS DOWN")
				logger.debug("Real IP BLOCKED or the SITE IS DOWN")
				sys.exit(0)

		time.sleep(5)



if __name__ == "__main__":
	start()
