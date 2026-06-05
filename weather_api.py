# 날씨 요청 함수들

import os
import math
import requests
from datetime import datetime, timedelta

# 강수 형태 매핑을 위한 딕셔너리
PTY_CODE = {
    "0": "강수 없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울/눈날림",
    "7": "눈날림"
}

# ===============================
# [1] 기상청 초단기 실황 api에 넣을 기준 날짜와 기준 시간을 자동으로 만들어주는 함수 
# ===============================
def get_base_time_for_ncst():
    now = datetime.now()

    # 초단기실황은 정시 기준 자료라, 안정적인 데이터 로드를 위해 너무 이른 시각이면 이전 시간 사용
    if now.minute < 40:
        now = now - timedelta(hours=1)

    return now.strftime("%Y%m%d"), now.strftime("%H00")


# ===============================
# [2] 위도, 경도를 기상청 전용 격자 좌표로 바꿔주는 함수
# ===============================
def convert_lat_lon_to_grid(lat, lon):
    # 지구 반지름
    RE = 6371.00877

    # 격자 간격 5km
    GRID = 5.0

    # 투영 계산에 쓰는 기준 위도
    SLAT1 = 30.0
    SLAT2 = 60.0

    # 기준 경도
    OLON = 126.0

    # 기준 위도
    OLAT = 38.0

    # 기준점의 격자 좌표 보정값
    XO = 43
    YO = 136

    # 도 단위를 라디언으로 바꿈
    DEGRAD = math.pi / 180.0

    # 지구 반지름을 격자 단위로 환산 -> 지구 반지름 km /  격자 간격 5km
    re = RE / GRID

    # 투영 계산용 보정값 (지구는 둥그니까 지도로 펼칠 때 생기는 왜곡 보정)
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)

    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = (sf ** sn) * math.cos(slat1) / sn

    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / (ro ** sn)

    # 입력된 위도/경도를 위치로 변환
    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / (ra ** sn)

    # 경도 차이 계산
    theta = lon * DEGRAD - olon

    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi

    theta *= sn

    x = int(ra * math.sin(theta) + XO + 0.5)
    y = int(ro - ra * math.cos(theta) + YO + 0.5)

    return x, y


# ===============================
#  [3] 날씨 요청 함수
# ===============================
def get_korea_weather(location=None, latitude=None, longitude=None):

    # 환경변수에서 API 키와 요청 URL을 로드하고, 위경도를 기상청 격자 좌표로 변환
    weather_api_key = os.getenv("WEATHER_API_KEY")
    url = os.getenv("GET_KOREA_WEATHER")
    nx, ny = convert_lat_lon_to_grid(latitude, longitude)

    # 기상청 초단기실황 조회 기준일자 및 기준시각 계산
    base_date, base_time = get_base_time_for_ncst()
    
    # 기상청 API 요청 파라미터 구성
    params = {
        "serviceKey": weather_api_key,
        "pageNo": 1,
        "numOfRows": 100,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    # 기상청 API에 GET 요청 전송  
    response = requests.get(url, params=params)
    print("status_code:", response.status_code)
    # print("response preview:", response.text[:300]) # response의 모든 정보 

    # JSON 응답 파싱
    data = response.json()

    # 응답 헤더를 확인하여 API 처리 결과 검증
    header = data["response"]["header"]
    if header["resultCode"] != "00":
        return f"기상청 API 오류: {header['resultCode']} / {header['resultMsg']}"

    # 응답 본문에서 관측 항목 리스트 추출
    items = data["response"]["body"]["items"]["item"]

    # category 코드를 key로, obsrValue를 value로 매핑
    weather_info = {}
    for item in items:
        weather_info[item["category"]] = item["obsrValue"]

    # 기온
    temp = weather_info.get("T1H")  

    # 습도
    humidity = weather_info.get("REH")  

    # 강수형태
    rain_type = PTY_CODE.get(weather_info.get("PTY"), weather_info.get("PTY"))  

    # 1시간 강수량
    rain_1h = weather_info.get("RN1")  

    # 풍속
    wind_speed = weather_info.get("WSD")  
    
    # 사용자에게 전달할 날씨 응답 문자열 생성
    return (
        f"{location}의 기상청 초단기실황입니다. "
        f"기온은 {temp}℃, 습도는 {humidity}%, 강수형태는 {rain_type}, "
        f"1시간 강수량은 {rain_1h}mm, 풍속은 {wind_speed}m/s입니다. "
        f"조회 기준시각은 {base_date} {base_time}, 격자좌표는 nx={nx}, ny={ny}입니다."
    )
