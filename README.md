# Azure-OpenAI-kma-Weather-bot
Azure OpenAI와 기상청 API를 활용해 사용자의 날씨 질문에 답변하는 날씨 응답 챗봇입니다.

# 날씨 응답 챗봇

기상청 API와 Azure OpenAI 수업 내용을 바탕으로 만든 날씨 응답 챗봇입니다.
사용자가 지역 날씨를 질문하면 기상청 API에서 데이터를 가져와 챗봇 형식으로 응답합니다.

## 주요 기능

- 기상청 API를 활용한 날씨 데이터 요청
- 사용자 질문 기반 날씨 응답 생성
- 터미널 실행 지원
- Streamlit 기반 웹 화면 제공

## 프로젝트 구조

```text
weather-chatbot/
├─ main.py
├─ weather_api.py
├─ chatbot.py
├─ streamlit_app.py
├─ requirements.txt
├─ README.md
└─ notebooks/
   └─ chatbot_test.ipynb

## 주요 함수

- `transcribe_audio()`  
  사용자 음성 입력을 텍스트로 변환합니다.

- `generate_chat_response()`  
  사용자 질문을 Azure OpenAI Assistant에 전달하고, 필요 시 기상청 API 함수를 호출하여 답변을 생성합니다.

- `get_korea_weather()`  
  기상청 초단기실황 API를 호출하여 지역별 현재 날씨 정보를 반환합니다.

- `synthesize_speech()`  
  챗봇 답변 텍스트를 음성 파일로 변환합니다.