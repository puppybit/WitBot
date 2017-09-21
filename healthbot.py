#-*- coding: utf-8 -*-
import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from pprint import pprint
import random

random.seed(3)

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

  if data['object'] == 'page':
    for entry in data['entry']:
      for messaging_event in entry['messaging']:

          # IDs
          sender_id = messaging_event['sender']['id']
          recipient_id = messaging_event['recipient']['id']

          messaging_text = None

          if messaging_event.get('message'):
            if 'text' in messaging_event['message']:
                messaging_text = messaging_event['message']['text']
            else:
                messaging_text = 'no text'

          #Echo
          #response = messaging_text

          response = None
          entity, value = wit_response(messaging_text)

          print(entity)
          print(value)

          #DM for healthbot

          if entity == 'intent_greeting':
            response = "반갑습니다. 저는 피트니스 프로그램과 헬스 악세사리를 선택하는데 도움을 드릴 수 있습니다."

          if entity == 'intent_recommend' and value == 'fit_program':
            response = "당신의 헬스앱 사용 패턴을 분석하여 최적의 피트니스 프로그램을 준비하였습니다. 보시겠습니까?"

          if entity == 'intent_recommend' and value == 'health_acc':
            response = "추천하는 헬스 악세사리 입니다. \n 1.삼성 기어 S3 \n 2. 삼성 기어핏 \n 3. Mi Smart Scales"

          if entity == 'intent_positive':
            type = random.randrange(1,3)
            if type == 1:
              response = "달리기를 자주하셨군요. 10 킬로미터 달리기 프로그램을 바로 시작하세요"
            elif type == 2:
              response = "다이어트에 관심이 많으시군요. 체중 감량 프로그램 중 기초부터 시작하는 적응 훈련을 해보세요."
            elif type == 3:
              response = "당신에게 필요한 근지구력 강화하기 프로그램을 준비하였습니다."

          if entity == 'intent_negative':
            response = "네 알겠습니다."

          if response == None:
            response = "죄송합니다. 제가 이해할수 없는 말입니다."

          bot.send_text_message(sender_id, response)


  return "ok", 200


def log(message):
  pprint(message)
  sys.stdout.flush()



if __name__ == "__main__":
  app.run(debug = True, port = 2020)

