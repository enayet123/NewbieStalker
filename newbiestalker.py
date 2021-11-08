#!/usr/bin/env python3

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SLACK_URL = os.getenv('SLACK_URL')
PAGE_URL = os.getenv('PAGE_URL')
SLEEP = 300 if not os.getenv('SLEEP') else int(os.getenv('SLEEP'))

def slack(msg):
	r = requests.post(SLACK_URL, json={'text': msg}, headers={'Content-Type': 'application/json'})

def printMsg(msg, slackMsg=False):
        print("[", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "]", msg)
        if (slackMsg):
                slack(msg)

def createMsg(name, logo, symbol, price, p1h, p24h, blockchain):
	return ":alert: " + name + " [" + symbol + "] " + price + " - " + blockchain + " :alert:"

headers = {'Host': 'coinmarketcap.com', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36', 'Connection': 'close'}
init = False
printMsg("Running...")
existing = {} 

while True:
	printMsg("Iterating...")
	page = requests.get(PAGE_URL, headers=headers)
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find_all("tr")
	table.pop(0)
	for i in table:
		symbol = i.find_all("p", {"class": "coin-item-symbol"})[0].text
		if symbol in existing:
			continue
		name = i.find_all("p", {"class": "sc-1eb5slv-0"})[1].text
		logo = i.find_all("img", {"class": "coin-logo"})[0]['src']
		tabledata = i.find_all("td")
		price = tabledata[3].text
		delta1h = tabledata[4].text
		delta24h = tabledata[5].text
		blockchain = tabledata[8].text
		slackmsg = createMsg(name, logo, symbol, price, delta1h, delta24h, blockchain)
		printMsg(slackmsg, init)
		existing[symbol] = True
	json.dump(existing, open('.data', 'w'))
	init = True
	time.sleep(SLEEP)
