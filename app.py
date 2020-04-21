from flask import Flask, request
from pymessenger.bot import Bot
import random
from dataCleaning import queryingData
import os
import dataScrape

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

dataScrape.getData()

@app.route('/')
def homepage():
    return 'Covid Chatbot PH by Rane'

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
    app.run()