import json
import requests
from bs4 import BeautifulSoup
import threading
import time


# json_data를 클래스로 변환
class JsonData:
    def __init__(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, value)
    # 클래스를 json 파일로 다시 저장
    def save(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=4)

    # 클래스 속성 추가
    def add(self, key, value):
        setattr(self, key, value)

    #클래스 속성 리스트 보기
    def show(self):
        for key, value in self.__dict__.items():
            print(key, value)

    #속성 키 값으로 삭제하기
    def delete(self, key):
        delattr(self, key)
    
def line_post(message, config):
    try:
        api_url = 'https://notify-api.line.me/api/notify'
        token = config.token
        headers = {'Authorization': 'Bearer ' + token}
        payload = {'message': message}
        r = requests.post(api_url, headers=headers, params=payload)
        print(r.text)
    except Exception as e:
        print(e)


def main(config):
    #현재 년/월/일/시/분/초 표시
    now = time.localtime()
    now_time = '%04d/%02d/%02d %02d:%02d:%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    
    #현재 시간이 오전 7시 ~ 8시 사이 일 때
    if now.tm_hour == 7:
        #호랑이 띠 운세
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%ED%98%B8%EB%9E%91%EC%9D%B4%EB%9D%A0%20%EC%9A%B4%EC%84%B8'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        t_rst = soup.find('p', {'class': 'text _cs_fortune_text'}).text

        #토끼띠 운세
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%ED%86%A0%EB%81%BC%EB%9D%A0%20%EC%9A%B4%EC%84%B8'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        r_rst = soup.find('p', {'class': 'text _cs_fortune_text'}).text

        #합치기
        sum_t_r_rst = f"호랑이띠 운세 : {t_rst}\n\n토끼띠 운세 : {r_rst}"

        msg = sum_t_r_rst
        
        print(msg)
        line_post(message = msg, config = config)
    timer = threading.Timer(600, main, [config])
    timer.start()

if __name__ == '__main__':

    #json 파일 로드
    with open('config.json', 'r', encoding= 'utf-8') as f:
        json_data = json.load(f)

    config = JsonData(json_data)


    main(config)


