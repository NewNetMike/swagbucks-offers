import requests
import json5
from discord import Webhook, SyncWebhook
from discord import Embed
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import os
import requests
import psycopg2
import os

from database import *

try:
    import config
except:
    pass

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = config.DATABASE_URL

try:
    WEBHOOK_URL = os.environ['WEBHOOK_URL']
except:
    WEBHOOK_URL = config.WEBHOOK_URL

try:
    H = os.environ['H']
except:
    H = config.H

try:
    PINGROLE = os.environ['PINGROLE']
except:
    PINGROLE = config.PINGROLE

try:
    ICON_URL = os.environ['ICON_URL']
except:
    ICON_URL = config.ICON_URL

try:
    TITLE = os.environ['TITLE']
except:
    TITLE = config.TITLE

connection = psycopg2.connect(DATABASE_URL, sslmode='require')
db = Database(connection=connection)

headers = {
    'authority': 'www.swagbucks.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.swagbucks.com',
    'referer': 'https://www.swagbucks.com/discover/featured',
    'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

valid_cards = []
cards = []
index = 0

data = {
    'h': H,
    'lastPos': '0',
    'pseudoCards': '',
    'sort': '4',
}

while True:

    params = {
        'cmd': 'card-jx-more',
        'streamID': '120',
        'count': '65',
        'startindex': str(index),
        'displayedMB': 'false',
    }

    response = requests.post('https://www.swagbucks.com/', params=params, headers=headers, data=data)
    print(response.text)

    jdata = json5.loads(response.text[2:])
    index = jdata["nextIndex"]
    new = 0
    for card in jdata["cards"]:
        cardId = card["cardId"]
        if cardId not in cards:
            cards.append(cardId)
            new += 1
        else:
            print("Already in there!")

        try:
            if card["shareData"]["referralBonus"] > 0:
                valid_cards.append(card)
        except:
            print("no referral Bonus :(")
    if new <= 0 or 1==1:
        print("NO NEW ONES FOUND!!")
        break

for card in valid_cards:
    exists = db.getSB(str(card["cardId"]))
    if exists:
        continue
    the_url = card["shareData"]["referralUrl"].split("&rb")[0] + "&rb=119678156"

    webhook = SyncWebhook.from_url(WEBHOOK_URL)

    dollar_amount = card["shareData"]["currencyAmount"]
    dollar = "${:.2f}".format(dollar_amount)

    embed = Embed(title=dollar + " - " + card["header"], description=card["subHeader"], color=random.randint(0, 0xFFFFFF), url=the_url)
    embed.set_author(name=TITLE, icon_url=ICON_URL)
    embed.set_image(url=card["image600x300"])
    embed.add_field(name="Go to this offer on swagbucks:", value=the_url)
    #embed.set_footer(text="dealmonitor.xyz", icon_url="https://i.pinimg.com/originals/4b/5f/b3/4b5fb3ba49cd624fb84f784ef047e8ee.jpg")
    webhook.send(embed=embed, content=PINGROLE)

    db.saveSB(str(card["cardId"]))


