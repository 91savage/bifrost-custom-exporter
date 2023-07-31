import requests
import json

## 빗썸 API
url = "https://api.bithumb.com/public/ticker/BFC_KRW"

## http 요청 헤더 정의, JSON 형식의 응답을 받기 위해 accpt 헤더를 아래와 같이 설정
headers = {"accept": "application/json"}

# request GET 메소드로 API에 HTTP요청을 보내고 응답을 response 변수에 저장
response = requests.get(url, headers=headers)

## HTTP 응답으로 받은 데이터를 문자열 형태로 priceData 변수에 저장
priceData = response.text

## json.loads() 함수를 사용하여 priceData를 Json형식으로 파싱하여 파이썬 데이터 구조로 변환
parsedData = json.loads(priceData)

## 현재 가격
currentPrice = parsedData['data']['closing_price']

