import os
import base64
import json
import requests
import time
from openai import AzureOpenAI
from dotenv import load_dotenv 
from weather_api import get_korea_weather
from weather_location import extract_location

load_dotenv()

LOCATION_COORDS = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
    "인천": (37.4563, 126.7052),
    "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845),
    "울산": (35.5384, 129.3114),
    "세종": (36.4800, 127.2890),
    "제주": (33.4996, 126.5312),
}



# 사용자가 입력한 메시지 개수
messages_limit = 6

# ????????????????
messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "너는 날씨정보를 기상청으로부터 받아와서 사용자에게 친절하게 답변하는 챗봇이야."
                }
            ]
        }]


# ==========================
# 날씨 알려주는 챗봇 함수
# ==========================
def generate_chat_response(user_input):
    #------------
    # 환경변수에서 API 키와 요청 URL을 로드
    #------------
    endpoint = os.getenv("ENDPOINT_URL")
    deployment = os.getenv("DEPLOYMENT_NAME")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version= os.getenv("OPEN_API_VERSION")

    #------------
    # 키인증 방식으로 Azure 클라이언트 객체 만들기
    #------------
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version
    )

    # 주요 도시 날씨 정보에 답변하기
    location = extract_location(user_input)

    if "날씨" in user_input and location:
        latitude, longitude = LOCATION_COORDS[location]

        weather_result = get_korea_weather(
            location=location,
            latitude=latitude,
            longitude=longitude
        )

        user_message = f"""
사용자 질문: {user_input}

아래는 기상청 API 조회 결과야.
이 정보를 바탕으로 사용자에게 자연스럽게 답변해줘.

{weather_result}
"""
    elif "날씨" in user_input and location is None:
        user_message = f"""
사용자가 날씨를 물어봤지만 지원하는 지역명을 찾지 못했어.
현재 지원 지역은 서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 제주야.
사용자에게 지원 지역명을 포함해서 다시 질문해달라고 안내해줘.
"""
    else:
        user_message = user_input

    global messages

    messages.append(
        {
            "role": "user",
            "content": [{"type": "text", "text": user_message}]
        }
    )

    if len(messages) > (1 + messages_limit):
        messages = [messages[0]] + messages[-messages_limit:]

    #------------
    # GPT 호출하기
    #------------
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=6553,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    #----------------
    #  response를 변수로 저장해서, messages에 assistant 역할로 추가하기
    #----------------
    response = completion.choices[0].message.content

    messages.append(
        {"role": "assistant",
        "content": [{"type": "text", "text": response}]
        }
    )
    
    return response
