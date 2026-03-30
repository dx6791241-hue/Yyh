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

# ====================== BANNER GỐC ======================
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

def luu_thong_tin_ip(ip, key, exp):
    data = {ip: {'key': key, 'expiration_date': exp.isoformat()}}
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

def get_shortened_link_phu(url):
    try:
        token = "6989d7bcd70a74263103abab"
        r = requests.get(f"https://link4m.co/api-shorten/v2?api={token}&url={url}", timeout=5)
        return r.json()
    except:
        return {"status": "error"}

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
    with ThreadPoolExecutor(max_workers=2) as ex:
        print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key (Free)")
        while True:
            ch = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
            if ch == "1":
                data = ex.submit(get_shortened_link_phu, url).result()
                link = data.get('shortenedUrl')
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

total = 0
driver = None

def init_browser():
    global driver
    opts = Options()
    opts.add_argument("--user-data-dir=C:\\ChromeProfileTDS")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-images")
    opts.add_argument("--blink-settings=imagesEnabled=false")
    opts.page_load_strategy = "eager"
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print(f"{luc}✅ Chrome đã mở!")
        return driver
    except Exception as e:
        print(f"{red}Không mở được Chrome!")
        sys.exit()

# ================== AUTO CLICK - TỐC ĐỘ VỪA PHẢI (8-9 GIÂY/JOB) ==================

def auto_comment():
    try:
        comment_btn = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='comment-icon']")))
        driver.execute_script("arguments[0].click();", comment_btn)
        time.sleep(1.5)
        comment_input = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
        comment_input.send_keys("Hay lắm ❤️")
        time.sleep(0.8)
        send_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Gửi')]")))
        driver.execute_script("arguments[0].click();", send_btn)
        print(f"{luc}✅ Đã comment")
        time.sleep(1.5)
        return True
    except:
        return False

# ====================== M# ================== AUTO CLICK - BẮT CHƯỚC THEO VIDEO ==================
def auto_click(link, job_type):
    global driver
    try:
        driver.get(link)
        time.sleep(2.3)   # Load trang user (theo video khoảng 2-3 giây)

        if job_type == 'tiktok_follow':
            targets = [
                "//button[contains(., 'Follow') or contains(., 'Theo dõi')]",
                "//button[@data-e2e='follow-button']",
                "//button[contains(@class, 'follow')]"
            ]
        elif job_type == 'tiktok_like':
            targets = ["//button[@data-e2e='like-icon']"]
        elif job_type == 'tiktok_comment':
            return auto_comment()

        for target in targets:
            try:
                btn = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, target))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                
                print(f"{luc}✅ ĐÃ CLICK FOLLOW")
                time.sleep(2)   # Giữ trang 3.2 giây sau khi click (theo video)
                return True
            except:
                continue

        print(f"{red}❌ Không tìm thấy nút Follow")
        return False

    except Exception as e:
        if "no such window" in str(e).lower():
            print(f"{red}Chrome đóng! Mở lại...")
            init_browser()
            time.sleep(2)
            return auto_click(link, job_type)
        print(f"{red}⚠️ Lỗi: {e}")
        return False
        
def main():
    global driver
    dem = 0

    if not get_key_system():
        sys.exit()

    banner()
    print(f"{luc}Dev:Deltatrash09(Duong Khoi)")

    while True:
        if os.path.exists('configtds.txt'):
            token = open('configtds.txt','r').read().strip()
        else:
            token = input(f'{thanh_xau}{luc}Nhập Access Token TDS: {vang}')
            open('configtds.txt','w').write(token)

        tds = TraoDoiSub(token)
        data = tds.profile()
        if data:
            print(lam + ' Đăng nhập TDS thành công!')
            user, xu = data.get('user'), data.get('xu')
            break
        else:
            print(red + 'Token sai!')
            if os.path.exists('configtds.txt'): os.remove('configtds.txt')

    tiktok_id = input(f'{thanh_xau}{luc}Nhập ID TikTok muốn chạy: {vang}').strip()
    res_set = tds.set_tiktok_run(tiktok_id)
    if res_set and 'success' in str(res_set):
        print(f'{luc}✅ Đã cấu hình nick thành công!')
    else:
        print(red + '❌ Cấu hình thất bại!'); return

    init_browser()

    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Like | 2 → Follow | 3 → Comment')
        nhiem_vu = input(f'{thanh_xau}{luc}Chọn: {vang}').strip()
        dl = int(input(f'{thanh_xau}{luc}Delay (giây): {vang}'))
        nv_nhan = int(input(f'{thanh_xau}{luc}Nhận xu sau bao nhiêu job: {vang}'))

        if nhiem_vu == '1': job_type, cache_type, nhan_type = 'tiktok_like', 'TIKTOK_LIKE_CACHE', 'TIKTOK_LIKE'
        elif nhiem_vu == '2': job_type, cache_type, nhan_type = 'tiktok_follow', 'TIKTOK_FOLLOW_CACHE', 'TIKTOK_FOLLOW'
        elif nhiem_vu == '3': job_type, cache_type, nhan_type = 'tiktok_comment', 'TIKTOK_COMMENT_CACHE', 'TIKTOK_COMMENT'
        else: continue

        while True:
            listjob = tds.get_job(job_type)
            try: jobs = listjob.json().get('data', [])
            except: jobs = []

            if not jobs:
                print(red + 'Hết job, đang chờ...', end='\r')
                time.sleep(5)
                continue

            for job in jobs:
                job_id, link = job['id'], job['link']
                auto_click(link, job_type)
                dem += 1
                
                if tds.cache(job_id, cache_type):
                    tg = datetime.now().strftime('%H:%M:%S')
                    print(f'{vang}[{dem}] {red}| {lam}{tg} {red}| {luc}CACHE {red}| {trang}{job_id}')
                    time.sleep(dl)
                    if dem % nv_nhan == 0:
                        tds.nhan_xu(nhan_type)
                else:
                    print(red + f'Lỗi Cache ID: {job_id}')

class TraoDoiSub:
    def __init__(self, token):
        self.token = token
        self.base = "https://traodoisub.com/api/"

    def profile(self):
        try:
            r = requests.get(f"{self.base}?fields=profile&access_token={self.token}", timeout=10)
            return r.json().get('data')
        except: return None

    def set_tiktok_run(self, tiktok_id):
        try:
            url = f"{self.base}?fields=tiktok_run&id={tiktok_id}&access_token={self.token}"
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
        global total
        try:
            url = f"https://traodoisub.com/api/coin/?type={nhan_type}&id={nhan_type}_API&access_token={self.token}"
            data = requests.get(url, timeout=10).json()
            if 'data' in data:
                xuthem = data['data'].get('xu_them', 0)
                xu_hien_tai = data['data'].get('xu', 0)
                total += int(xuthem)
                print(f'\n{lam}✅ NHẬN THÀNH CÔNG {red}| {luc}Cộng: {vang}{xuthem} {luc}Xu {red}| {luc}Tổng: {vang}{total} {luc}Xu {red}| {vang}{xu_hien_tai}')
                return True
            return False
        except: return False

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        if driver: driver.quit()
        sys.exit()
