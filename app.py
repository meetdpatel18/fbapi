import os, sys, json
from flask import Flask, request
from pprint import pprint
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN ="EAAGUA4KSDscBALThBptXdRxvu0htfksIyaarz45vSHrUoVpcLaTkuZAx2TOZBZAOrNiQjetyGJZAFCudZAUB0TB9dpMkwLLKYHzQ97A36XjnPWZCeIDOJyefNeZCuZBlBDTxTfRopOM8VVN2MW4p3j8LV2PVzozWU0UWQ1qqTEJqU0WWB1xTXJrB"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

@app.route('/',methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                #Fetching Sender Id
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                #Fetching the message from the json object
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                    
                    #Echoing the text
                    response = messaging_event
                    bot.send_text_message(sender_id, messaging_text)

    return "ok", 200

def log(message): 
    pprint(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True, port = 80)