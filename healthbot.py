#-*- coding: utf-8 -*-
import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from pprint import pprint

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAZAMuyRdo2EBAPAnwdKdG5k7KfgeZBtWDHLOwGo77g6d0dkFvuDzwfzTP8KNhFadKw7Hq84zeOH9cFmbJ2ZC3GwsaWBEqhGTHyo4Iwkn9VpNG82tfPOQF1HaOhPgyZAAyP5sEtROVF0ZBtAwlazZAa8jcw3srBsSOxZBJU6Xbv2YU4JNaaotvv"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def verify():
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    if not request.args.get("hub.verify_token") == "hello":
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200
  return "Hello World!", 200

@app.route("/", methods=['POST'])
def webhook():
  data = request.get_json()
#  log(data)

  if data['object'] == 'page':
    for entry in data['entry']:
      for messaging_event in entry['messaging']:

          # IDs
          sender_id = messaging_event['sender']['id']
          recipient_id = messaging_event['recipient']['id']

          if messaging_event.get('message'):
            if 'text' in messaging_event['message']:
                messaging_text = messaging_event['message']['text']
            else:
                messaging_text = 'no text'

          #Echo
          #response = messaging_text

          entity, value = wit_response(messaging_text)

          #DM for healthbot

          if entity == 'intent_greeting':
            response = "반갑습니다. 무엇을 도와드릴까요?"

          if entity == 'intent_recommend' and value == 'fit_program':
            response = "어떤 프로그램을 추천해 드릴까요?"

          if entity == 'intent_recommend' and value == 'health_acc':
            response = "헬스와 연결 가능한 악세사리 리스트 입니다."

          if response == None:
            response = "죄송합니다. 제가 이해할수 없는 말입니다."

          bot.send_text_message(sender_id, response)


  return "ok", 200


def log(message):
  pprint(message)
  sys.stdout.flush()



if __name__ == "__main__":
  app.run(debug = True, port = 2020)

