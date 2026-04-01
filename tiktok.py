# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import time
import base64
import random
from datetime import datetime
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

# ====================== GET KEY (đầy đủ + link4m) ======================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    with open('ip_key.json', 'w') as file:
        file.write(encrypt_data(json.dumps(data)))

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'HECTORVN{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://deltagetkey.blogspot.com/2026/02/get-key.html?ma={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    try:
        token = "6989d7bcd70a74263103abab"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=8)
        if response.status_code == 200:
            return response.json()
        return {"status": "error"}
    except:
        return {"status": "error"}

def get_key_system():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if not ip_address:
        print(f"{red}Không lấy được IP!")
        sys.exit()

    existing_key = kiem_tra_ip(ip_address)
    if existing_key:
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn...")
        sleep(2)
        return True

    url, key, expiration_date = generate_key_and_url(ip_address)

    with ThreadPoolExecutor(max_workers=2) as executor:
        print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key (Free)")

        while True:
            choice = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
            if choice == "1":
                data = executor.submit(get_shortened_link_phu, url).result()
                link_key = data.get('shortenedUrl', url)
                print(f'\033[1;35mLink Để Vượt Key: {link_key}')

                while True:
                    keynhap = input('\033[1;33mKey Đã Vượt Là: ')
                    if keynhap == key or keynhap == "hectoradminskibidi123":
                        print(f'{luc}Key Đúng!')
                        sleep(1.5)
                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                        return True
                    else:
                        print(f'{red}Key Sai!')

# ====================== UNDETECTED CHROMEDRIVER (Fix version) ======================
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

total = 0
driver = None

def init_browser():
    global driver
    try:
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=C:\\ChromeProfileTDS")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-images")

        # Ép đúng phiên bản Chrome 146 của mày
        driver = uc.Chrome(
            options=options,
            use_subprocess=True,
            version_main=146
        )
        
        print(f"{luc}✅ Undetected Chrome mở thành công (version 146)!")
        return driver
    except Exception as e:
        print(f"{red}❌ Không mở được Chrome: {e}")
        sys.exit()

# ====================== AUTO CLICK + F5 ======================
def auto_click(link, job_type):
    global driver
    try:
        driver.get(link)
        time.sleep(4.0)

        if job_type == 'tiktok_follow':
            targets = [
                "//button[contains(., 'Follow') or contains(., 'Theo dõi')]",
                "//button[@data-e2e='follow-button']",
                "//button[contains(@class, 'follow')]",
                "//button[@aria-label='Follow' or @aria-label='Theo dõi']"
            ]

            for target in targets:
                try:
                    btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, target)))
                    
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(btn, random.randint(-20, 20), random.randint(-15, 15))
                    actions.pause(random.uniform(0.4, 0.8))
                    actions.move_to_element(btn)
                    actions.pause(random.uniform(0.5, 1.0))
                    actions.click()
                    actions.perform()
                    
                    print(f"{luc}✅ ĐÃ CLICK FOLLOW")
                    time.sleep(5.5)

                    print(f"{lam}🔄 Đang F5 kiểm tra...")
                    driver.refresh()
                    time.sleep(4.0)

                    still_follow = driver.find_elements(By.XPATH, "//button[contains(., 'Follow') or contains(., 'Theo dõi')]")
                    if still_follow:
                        print(f"{red}❌ Fake Click!")
                    else:
                        print(f"{luc}✅ Follow đã được ghi nhận THẬT!")
                    return True
                except:
                    continue

        print(f"{red}❌ Không tìm thấy nút Follow")
        return False

    except Exception as e:
        if "no such window" in str(e).lower():
            print(f"{red}⚠️ Chrome đóng! Mở lại...")
            init_browser()
            return auto_click(link, job_type)
        print(f"{red}⚠️ Lỗi: {e}")
        return False

# ====================== CLASS TRAODOISUB ======================
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
            url = f"{self.base}coin/?type={nhan_type}&id={nhan_type}_API&access_token={self.token}"
            data = requests.get(url, timeout=10).json()
            if 'data' in data:
                xuthem = data['data'].get('xu_them', 0)
                xu_hien_tai = data['data'].get('xu', 0)
                total += int(xuthem)
                print(f'\n{lam}✅ NHẬN THÀNH CÔNG {red}| {luc}Cộng: {vang}{xuthem} {luc}Xu {red}| {luc}Tổng: {vang}{total} {luc}Xu {red}| {vang}{xu_hien_tai}')
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
    print(f"{luc}Tool TikTok TDS - Undetected Chrome")

    while True:
        if os.path.exists('configtds.txt'):
            with open('configtds.txt', 'r') as f: 
                token = f.read().strip()
        else:
            token = input(f'{thanh_xau}{luc}Nhập Access Token TDS: {vang}')
            with open('configtds.txt', 'w') as f: 
                f.write(token)

        tds = TraoDoiSub(token)
        data = tds.profile()
        if data:
            print(lam + ' Đăng nhập TDS thành công!')
            user, xu = data.get('user'), data.get('xu')
            break
        else:
            print(red + 'Token sai!')
            if os.path.exists('configtds.txt'): 
                os.remove('configtds.txt')

    tiktok_id = input(f'{thanh_xau}{luc}Nhập ID TikTok muốn chạy: {vang}').strip()
    res_set = tds.set_tiktok_run(tiktok_id)
    if res_set and 'success' in str(res_set):
        print(f'{luc}✅ Đã cấu hình nick thành công!')
    else:
        print(red + '❌ Cấu hình nick thất bại!'); return

    init_browser()

    print(f"\n{red}╔════════════════════════════════════════════════════════════╗")
    print(f"{red}║ ⚠️ CẢNH BÁO: Delay khuyến nghị ≥ 4 giây                   ║")
    print(f"{red}║ Xóa C:\\ChromeProfileTDS trước khi chạy acc mới           ║")
    print(f"{red}╚════════════════════════════════════════════════════════════╝\n")

    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Like | 2 → Follow | 3 → Comment')
        
        nhiem_vu = input(f'{thanh_xau}{luc}Chọn: {vang}').strip()
        dl = int(input(f'{thanh_xau}{luc}Delay (giây) [Khuyến nghị 4]: {vang}') or 4)
        nv_nhan = int(input(f'{thanh_xau}{luc}Nhận xu sau bao nhiêu job: {vang}'))

        if nhiem_vu == '1': job_type, cache_type, nhan_type = 'tiktok_like', 'TIKTOK_LIKE_CACHE', 'TIKTOK_LIKE'
        elif nhiem_vu == '2': job_type, cache_type, nhan_type = 'tiktok_follow', 'TIKTOK_FOLLOW_CACHE', 'TIKTOK_FOLLOW'
        elif nhiem_vu == '3': job_type, cache_type, nhan_type = 'tiktok_comment', 'TIKTOK_COMMENT_CACHE', 'TIKTOK_COMMENT'
        else: continue

        print(f"{red}⚠️ Đang chạy {job_type.upper()}...")

        while True:
            listjob = tds.get_job(job_type)
            try: 
                jobs = listjob.json().get('data', [])
            except: 
                jobs = []

            if not jobs:
                print(red + 'Hết job, chờ 8 giây...', end='\r')
                time.sleep(8)
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

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        if driver: driver.quit()
        sys.exit()
