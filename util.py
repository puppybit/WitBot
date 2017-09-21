#-*- coding: utf-8 -*-

from wit import Wit

access_token = "T52D5PPBO5HVGSVZGUUR4OORBSZDD26U"

client = Wit(access_token = access_token)

message_text = "활동적인 하루 목표 설정하고 싶어"

resp = client.message(message_text)

print(resp)

