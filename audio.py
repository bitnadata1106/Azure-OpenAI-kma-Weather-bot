# audio 함수 모음

import os
import requests
from IPython.display import Audio
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# ==========================
# [1] transcribe_audio(audio_file) 함수
#     사용자의 음성 입력을 텍스트로 출력
# ==========================
def transcribe_audio(audio_file):
    import os
    from openai import AzureOpenAI
    from dotenv import load_dotenv

    load_dotenv()

    client = AzureOpenAI(
            api_key=os.getenv("IMAGE_VOICE_API_KEY"),  
            api_version=os.getenv("WISPER_API_VERSION"),
            azure_endpoint = os.getenv("IMAGE_VOICE_ENDPOINT_URL")
        )
        
    deployment_id = "whisper" #모델 이름
    audio_test_file = audio_file
        
    result = client.audio.transcriptions.create(
            file=open(audio_test_file, "rb"),
            model=deployment_id
        )
    
    return result.text


# ==========================
# [2] synthesize_speech(text, output_file="output.mp3") 함수
#     텍스트 입력을 음성으로 출력
# ==========================
def synthesize_speech(text, output_file="output.mp3"):

    url = os.getenv("TTS_ENDPOINT_URL")
    speech_apikey = os.getenv("IMAGE_VOICE_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "api-key": speech_apikey
    }

    payload = {
        "model": "gpt-4o-mini-tts",
        "input": text,
        "voice": "echo"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)

        return output_file
    else:
        print("TTS 실패!", response.status_code)
        print(response.text)
        return None