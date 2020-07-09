from flask import Flask, request, render_template
from pymessenger.bot import Bot
import random
from dataCleaning import queryingData
import os
import dataScrape, dataCleaning

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

bot = Bot(ACCESS_TOKEN)

dataScrape.getData()
cases = dataCleaning.queryingData().cases
active = dataCleaning.queryingData().active
deaths = dataCleaning.queryingData().deaths
recoveries = dataCleaning.queryingData().recovered
date = dataCleaning.queryingData().dateUpdated
newCases = dataCleaning.queryingData().todayCases
newDeaths = dataCleaning.queryingData().todayDeaths
newRecov = dataCleaning.queryingData().todayRecovered

@app.route('/')
def index():
    return render_template("index.html", cases=cases, active=active, deaths=deaths, recoveries=recoveries, date=date, newCases=newCases, newDeaths=newDeaths, newRecov=newRecov)

@app.route('/get-data/', methods = ['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output=request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        userMess = (message['message'].get('text'))
                        response_sent_text = get_message(userMess)
                        send_message(recipient_id, response_sent_text)
                    if message['message'].get('attachments'):
                        #print(message['message'].get('attachments'))
                        response_sent_nontext = ":)"
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message(userMess):
    q = queryingData()
    return(q.loadJson(userMess))

def send_message(recipient_id, response):
    #bot.send_text_message(recipient_id, response)
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run()