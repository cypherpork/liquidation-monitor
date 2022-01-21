#!/usr/bin/python

import smtplib, ssl, sys, os
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from configparser import ConfigParser
from subprocess import Popen, PIPE

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "config.conf")

if os.path.exists(config_path):
	cfg = ConfigParser()
	cfg.read(config_path)
else:
	print("Config not found! Exiting!")
	sys.exit(1)

show_help_list = cfg.getboolean("main", "show_help_list")
send_to_info_if_not_alerts = cfg.getboolean("main", "send_to_info_if_not_alerts")
lpv = cfg.get("main", "liquid_price_value")

user = cfg.get("twinkle", "user")
if user == "" :
	user = "makermon"

account = cfg.get("twinkle", "account")

url = cfg.get("web", "url")
wait = cfg.getfloat("web", "wait")

debug_level = cfg.getint("smtp", "debug_level")
port = cfg.getint("smtp", "port")
smtp_server = cfg.get("smtp", "smtp_server")
sender = cfg.get("smtp", "sender")
password = cfg.get("smtp", "password")
receivers = cfg.get("smtp", "receivers").split(",")

def send(sub, text):
	message = MIMEMultipart()
	message['From'] = sender
	message['TO'] = ','.join(receivers)
	message['Subject'] = sub
	message['Date'] = formatdate(localtime=True)
	message.attach(MIMEText(text,'plain'))
	context = ssl.create_default_context()
	server = smtplib.SMTP(smtp_server, port)
	server.set_debuglevel(debug_level)
	server.starttls()
	server.login(sender, password)
	server.sendmail(sender, receivers, message.as_string())
	server.quit()

def callTwinkle(user, account)
	proc = Popen(["twinkle", "-c"], stdin=PIPE, stdout=PIPE, bufsize=1)
	for line in iter(proc.stdout.readline, b''):
		print line
		if ("registration succeeded" in line):
 			proc.stdin.write("user "+user+"\n")
			proc.stdin.write("call "+account+"\n")
			if ("far end answered call" in line):
 				proc.stdin.write("bye\n")
				proc.stdin.write("quit\n")
			if ("reject" in line):
				proc.stdin.write("quit\n")
	proc.communicate()

options = Options()
options.set_headless()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless")

# driver = webdriver.Chrome(executable_path="",options=options)

driver = webdriver.Firefox(options=options)

driver.get(url)
sleep(wait)
items = driver.find_elements_by_tag_name("div")[0]
if show_help_list:
	print("src list help:")
	all_items = items.text.split("\n")
	i = 0
	while i < len(all_items):
		print(str(i)+" | "+all_items[i])
		i += 1

# Liquidation Price value:
if lpv == "" :
	liquid_price_value = items.text.split("\n")[14]
else:
	liquid_price_value = lpv

# Current Price
cur_price_value = items.text.split("\n")[19]

# Next Price:
next_price_value = items.text.split("\n")[21]

data = "Liquidation Price: "+liquid_price_value+"\r\nCurrent Price: "+cur_price_value+"\r\nNext Price: "+next_price_value+"\r\n"

print("---------------------------------------------------------------")
print(data)

if next_price_value.replace(',','').replace('$','') < liquid_price_value.replace(',','').replace('$','') :
	print("important alert!!!")
	send("important alert!!!", "Your alert price is greater than the next price\r\n"+data+"\r\n")
	if account != "" :
		callTwinkle(user, account)
else:
	print("no alerts...")
	if send_to_info_if_not_alerts:
		send("no alerts...", data+"\r\n")

print("---------------------------------------------------------------")
driver.close()
