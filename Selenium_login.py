#檢測session id紀錄時間
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class NCUE_login:
    def __init__(self):
        with open('NCUE_accounts.txt', 'r') as f:
            self.account = f.read().strip()
            self.password = f.read().strip()

    def login(self):
        # 創建一個 ChromeOptions 實例
        options = Options()
        # 如果需要無頭模式，可以取消註解下面這行
        # options.add_argument('--headless')

        # 創建一個 Service 實例，指定 ChromeDriverManager().install() 來創建 WebDriver
        service = Service(ChromeDriverManager().install())

        # 創建一個 WebDriver 實例
        driver = webdriver.Chrome(service=service, options=options)

        driver.get('https://apss.ncue.edu.tw/afair/book_view.php')

        time.sleep(3)

        account = self.account

        password = self.password

        account_input = driver.find_element(By.ID, 'Ecom_User_ID')
        password_input = driver.find_element(By.ID, 'Ecom_Password')
        account_input.send_keys(account)
        password_input.send_keys(password)

        # 登入
        login_button = driver.find_element(By.NAME, 'LoginButton')
        login_button.click()

        phpsessid = None
        for cookie in driver.get_cookies():
            if cookie['name'] == 'PHPSESSID':
                phpsessid = cookie['value']
                break

        print("PHPSESSID:", phpsessid if phpsessid else "Not found")

        print('done')

        driver.quit()

        return phpsessid