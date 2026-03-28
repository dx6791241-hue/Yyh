# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import time
import base64
from datetime import datetime, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor

den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lam = "\033[1;36m"

thanh_xau = red + "[" + trang + "=.=" + red + "] " + trang + "=> "

# ====================== BANNER ======================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r'''
                                                                           ,--.        
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  : |        
,---.'|  : '                     |  | :,'   ,---.    __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                     :  : ' :  '   ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |   ,---.     ,---. .;__,'  /  /   /   |'  | |' |/___/ \  | |:   |   \ | :        
|   ' '  ; :  /     \   /     \|  |   |  .   ; ,. :|  |   ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. | /    /  | /    / ':__,'| :  '   | |: :'  :  /   \   \  \: |'   ' ;.    ;        
|   | :  | '.    ' / |.    ' /   '  : |__'   | .; :|  | '     ;   \  ' .|   | | \   |        
'   : |  : ;'   ;   /|'   ; :__  |  | '.'|   :    |;  : |      \   \   ''   : |  ; .'        
|   | '  ,/ '   |  / |'   | '.'| ;  :    ;\   \  / |  , ;       \   `  ;|   | '`--'          
;   : ;--'  |   :    ||   :    : |  ,   /  `----'   ---'         :   \ |'   : |              
|   ,/       \   \  /  \   \  /   ---`-'                          '---" ;   |.'              
'---'         `----'    `----'                                          '---'      
'''
    for char in ban:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.005)

# ====================== GET KEY ======================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        return requests.get('https://api.ipify.org?format=json', timeout=5).json()['ip']
    except:
        return None

def display_ip_address(ip):
    if ip:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip}")

def luu_thong_tin_ip(ip, key, expiration):
    data = {ip: {'key': key, 'expiration_date': expiration.isoformat()}}
    with open('ip_key.json', 'w') as f:
        f.write(encrypt_data(json.dumps(data)))

def kiem_tra_ip(ip):
    try:
        with open('ip_key.json', 'r') as f:
            data = json.loads(decrypt_data(f.read()))
        if ip in data:
            exp = datetime.fromisoformat(data[ip]['expiration_date'])
            if exp > datetime.now():
                return True
    except:
        pass
    return False

def generate_key_and_url(ip):
    ngay = datetime.now().day
    key1 = str(ngay * 27 + 27)
    ip_num = ''.join(filter(str.isdigit, ip))
    key = f'HECTORVN{key1}{ip_num}'
    exp = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://deltagetkey.blogspot.com/2026/02/get-key.html?ma={key}'
    return url, key, exp

def get_shortened_link(url):
    try:
        token = "6989d7bcd70a74263103abab"
        r = requests.get(f"https://link4m.co/api-shorten/v2?api={token}&url={url}", timeout=5)
        return r.json().get('shortenedUrl')
    except:
        return None

def get_key_system():
    ip = get_ip_address()
    display_ip_address(ip)
    if not ip:
        print(f"{red}Không lấy được IP!"); sys.exit()

    if kiem_tra_ip(ip):
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn...")
        sleep(2)
        return True

    url, key, exp = generate_key_and_url(ip)
    print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key (Free)")

    with ThreadPoolExecutor(max_workers=2) as ex:
        while True:
            ch = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
            if ch == "1":
                link = ex.submit(get_shortened_link, url).result()
                if link:
                    print(f'\033[1;35mLink vượt key: {link}')
                while True:
                    k = input('\033[1;33mNhập key đã vượt: ')
                    if k == key or k == "hectoradminskibidi123":
                        print(f'{luc}Key đúng!')
                        sleep(1.5)
                        luu_thong_tin_ip(ip, k, exp)
                        return True
                    print(f'{red}Key sai!')

# ====================== SELENIUM ======================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None

def init_browser():
    global driver
    opts = Options()
    opts.add_argument("--user-data-dir=C:\\ChromeProfileTDS")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print(f"{luc}✅ Chrome đã mở!")
        return driver
    except Exception as e:
        print(f"{red}Không mở được Chrome!")
        sys.exit()

def auto_click_fb(link, job_type):
    global driver
    try:
        driver.get(link)
        sleep(7)

        if job_type == "facebook_follow":
            xpaths = ["//div[@aria-label='Theo dõi']", "//span[text()='Theo dõi']", "//button[contains(.,'Theo dõi')]"]
        elif job_type == "facebook_like":
            xpaths = ["//div[@aria-label='Thích']", "//span[text()='Thích']"]
        else:
            xpaths = ["//div[@role='button']"]

        for xp in xpaths:
            try:
                btn = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                sleep(0.5)
                driver.execute_script("arguments[0].click();", btn)
                print(f"{luc}✅ Đã click {job_type}")
                sleep(1.5)
                return True
            except:
                continue

        print(f"{red}❌ Không tìm thấy nút")
        return False

    except Exception as e:
        if "no such window" in str(e).lower():
            print(f"{red}Cửa sổ Chrome đóng, đang mở lại...")
            init_browser()
            sleep(3)
            return auto_click_fb(link, job_type)
        print(f"{red}Lỗi: {e}")
        return False

# ====================== CLASS TDS ======================
class TraoDoiSub:
    def __init__(self, token):
        self.token = token
        self.base = "https://traodoisub.com/api/"

    def profile(self):
        try:
            r = requests.get(f"{self.base}?fields=profile&access_token={self.token}", timeout=10)
            return r.json().get('data')
        except: return None

    def set_facebook_run(self, fb_id):
        try:
            url = f"{self.base}?fields=run&id={fb_id}&access_token={self.token}"
            return requests.get(url, timeout=10).json()
        except: return None

    def get_job(self, job_type):
        try:
            url = f"{self.base}?fields={job_type}&access_token={self.token}"
            return requests.get(url, timeout=10)
        except: return None

    def cache(self, job_id, cache_type):
        try:
            url = f"{self.base}coin/?type={cache_type}&id={job_id}&access_token={self.token}"
            r = requests.get(url, timeout=10)
            return "success" in r.text.lower() or "cache" in r.text.lower()
        except: return False

    def nhan_xu(self, nhan_type):
        try:
            url = f"{self.base}coin/?type={nhan_type}&id={nhan_type}_API&access_token={self.token}"
            data = requests.get(url, timeout=10).json()
            if 'data' in data:
                xuthem = data['data'].get('xu_them', 0)
                print(f'\n{luc}Nhận thành công | +{vang}{xuthem}{luc} Xu')
                return True
            return False
        except: return False

# ====================== MAIN ======================
def main():
    global driver
    dem = 0

    if not get_key_system():
        sys.exit()

    banner()
    print(f"{luc}Dev:Deltatrash09(Duong Khoi)")

    # Nhập Token TDS
    if os.path.exists('configtds.txt'):
        token = open('configtds.txt','r').read().strip()
    else:
        token = input(f'{thanh_xau}{luc}Nhập Access Token TDS: {vang}')
        open('configtds.txt','w').write(token)

    tds = TraoDoiSub(token)
    data = tds.profile()
    if not data:
        print(red + 'Token sai!')
        if os.path.exists('configtds.txt'): os.remove('configtds.txt')
        sys.exit()

    print(lam + ' Đăng nhập TDS thành công!')
    user = data.get('user')
    xu = data.get('xu')

    # Nhập ID Facebook
    fb_id = input(f'{thanh_xau}{luc}Nhập ID Facebook muốn chạy: {vang}').strip()
    res = tds.set_facebook_run(fb_id)
    if res and 'success' in str(res).lower():
        print(f'{luc}✅ Đã cấu hình Facebook ID thành công!')
    else:
        print(red + '❌ Cấu hình Facebook thất bại!')
        return

    init_browser()

    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Follow    | 2 → Like')
        chon = input(f'{thanh_xau}{luc}Chọn: {vang}').strip()
        dl = int(input(f'{thanh_xau}{luc}Delay (giây): {vang}'))
        nhan_sau = int(input(f'{thanh_xau}{luc}Nhận xu sau bao nhiêu job: {vang}'))

        if chon == '1':
            job_type = 'facebook_follow'
            cache_type = 'facebook_follow_cache'
            nhan_type = 'facebook_follow'
        elif chon == '2':
            job_type = 'facebook_like'
            cache_type = 'facebook_like_cache'
            nhan_type = 'facebook_like'
        else:
            continue

        while True:
            listjob = tds.get_job(job_type)
            try:
                jobs = listjob.json().get('data', [])
            except:
                jobs = []

            if not jobs:
                print(red + 'Hết job, đang chờ...', end='\r')
                sleep(10)
                continue

            for job in jobs:
                job_id = job['id']
                link = job['link']
                auto_click_fb(link, job_type)
                dem += 1

                if tds.cache(job_id, cache_type):
                    tg = datetime.now().strftime('%H:%M:%S')
                    print(f'{vang}[{dem}] {red}| {lam}{tg} {red}| {luc}CACHE {red}| {trang}{job_id}')
                    sleep(dl)
                    if dem % nhan_sau == 0:
                        tds.nhan_xu(nhan_type)
                else:
                    print(red + f'Lỗi cache ID: {job_id}')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if driver:
            driver.quit()
        sys.exit()
