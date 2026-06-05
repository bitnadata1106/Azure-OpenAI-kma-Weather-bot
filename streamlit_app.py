import streamlit as st

from audio_stt import request_audio
from chatbot import request_upgrade_chat
from audio_tts import request_tts


st.set_page_config(
    page_title="Azure OpenAI 날씨 음성 챗봇",
    page_icon="🌦️",
    layout="centered"
)

st.title("🌦️ Azure OpenAI 날씨 음성 챗봇")
st.write("음성으로 날씨를 물어보면, AI가 기상청 데이터를 조회해 답변합니다.")

st.divider()

if st.button("🎙️ 음성 질문하기"):
    with st.spinner("음성을 텍스트로 변환하는 중입니다..."):
        user_text = request_audio()

    st.subheader("🧑 사용자 질문")
    st.write(user_text)

    with st.spinner("AI가 답변을 생성하는 중입니다..."):
        answer_text = request_upgrade_chat(user_text)

    st.subheader("🤖 AI 답변")
    st.write(answer_text)

    with st.spinner("답변을 음성으로 변환하는 중입니다..."):
        audio_path = request_tts(answer_text)

    st.subheader("🔊 음성 답변")
    st.audio(audio_path)