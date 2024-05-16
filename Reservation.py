import Selenium_login
import json
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

def get_space(session, space_value):
    url = f'https://apss.ncue.edu.tw/afair/order_form.php?place_code={space_value}'
    base_url = 'https://apss.ncue.edu.tw/afair/'

    req = session.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    form_url = base_url + soup.find('form')['action']

    # 表單數據
    form_data = {
        'place_code': space_value,
        'no_vacancy': '0',
        'tel': '',  # 請替換為實際的聯絡電話
        'reason': ''  # 請替換為實際的申請事由 
    }

    response = session.post(form_url, data=form_data)
    print(response.text)

def reservation(session, month, day):

    # 格式化月份和日期
    month = f'{int(month):02d}'
    day = f'{int(day):02d}'
    
    url = f'https://apss.ncue.edu.tw/afair/book.php?year=2024&month={month}&day={day}'
    base_url = 'https://apss.ncue.edu.tw/afair/'

    # 使用 faker_useragent 生成隨機的 User-Agent
    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
        'referer': 'https://apss.ncue.edu.tw/afair/book.php'
    }

    req_book_date = session.get(url, headers=headers)
    soup = BeautifulSoup(req_book_date.text, 'html.parser')
    form_save_url = base_url + soup.find('form')['action']

    print(form_save_url)

    # 找到所有的時段圖片
    time_slots = soup.find_all('td', height="46")
    available_slots = []

    # 檢查每個時段是否可用
    for index, slot in enumerate(time_slots):
        try:
            slot.find('img')['title']
        except:
            available_slots.append(f"{8 + index}")

    # 輸出空閒時段
    print("可借用的時段:", [f"{slot}點" for slot in available_slots])

    if available_slots:
        # 讓用戶選擇時段
        selected_slots = input("請輸入你想預約的時段（用逗號分隔，如9,13,14）:").split(',')
        selected_slots = [slot.strip() for slot in selected_slots]

        form_reservation_data = {
            'year': '113',
            'month': str(month),
            'day': str(day),
            'cont': '0'
        }

        # 添加選擇的時段
        for slot in selected_slots:
            form_reservation_data.setdefault('hour[]', []).append(slot)

        print(form_reservation_data)

        form_response = session.post(form_save_url, data=form_reservation_data, headers=headers)
        print(form_response.text)
    else:
        print('當天無空閒時段')

def load_space(path):
    with open(path, 'r',encoding='utf-8') as f:
        space_dict = json.load(f)

    # 只列出包含 url 的空間名稱及對應索引
    space_options = [space for space in space_dict if 'url' in space]
    for i, space in enumerate(space_options):
        print(f'{i + 1}: {space["name"]}')
    return space_options

if __name__ == '__main__':
    start_time = time.time()
    space_options = load_space('NCUE_space.json')
    # 請使用者選擇空間
    print('\n')
    index = int(input('請選擇空間代號索引:')) - 1
    space_code = space_options[index]["value"]
        
    phpsessid = Selenium_login.NCUE_login().login() # 登入並取得PHPSESSID

    session = requests.Session()
    session.cookies.set('PHPSESSID', phpsessid) 

    get_space(session, space_code) # 取得空間資訊
    month = input('請輸入月份:')
    day = input('請輸入日期:')
    reservation(session, month, day) # 預約空間

    end_time = time.time()

    print('執行時間:', end_time - start_time)

    #TODO 1.user-agent使用fake-useragent
    #TODO 2.申請事由寫在NCUE_accounts裡面
    #TODO 3.在main函式用迴圈while檢查session id是否過期
