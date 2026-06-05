# 1차시도: 이전 대화내역 앞 3번째부터만 기억함. 
from generate_chat_response import generate_chat_response


def main():
    print("🌦️ Azure OpenAI 기상청 날씨 챗봇입니다.")
    print("날씨가 궁금한 지역을 입력해보세요.")
    print("종료하려면 '그만'을 입력하세요.")
    print("-" * 50)

    while True:
        user_input = input("user: ")

        if user_input.lower() in ["그만", "그만해", "종료", "끝", "stop"]:
            print("챗봇과의 대화를 종료합니다.")
            break

        response = generate_chat_response(user_input)

        print("bot:", response)
        print("-" * 50)


if __name__ == "__main__":
    main()