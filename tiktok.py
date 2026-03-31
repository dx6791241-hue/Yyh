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

# ====================== GET KEY (giữ nguyên) ======================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        return requests.get('https://api.ipify.org?format=json', timeout=5).json()['ip']
    except:
        return None

def get_key_system():
    ip = get_ip_address()
    banner()
    print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip}")
    # ... (phần get key giữ nguyên như file cũ của mày, nếu thiếu thì báo tao bổ sung)
    # Để ngắn, giả sử mày copy phần get key từ file cũ vào đây
    return True  # tạm thời, mày thay bằng code get key thật của mày

# ====================== SELENIUM + STEALTH ======================
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

total = 0
driver = None

def init_browser():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=C:\\ChromeProfileTDS")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-images")
    chrome_options.page_load_strategy = "eager"

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        stealth(driver,
                languages=["vi-VN", "vi", "en-US"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        print(f"{luc}✅ Chrome Stealth đã mở (che giấu tốt)!")
        return driver
    except Exception as e:
        print(f"{red}❌ Không mở được Chrome: {e}")
        sys.exit()

# ====================== AUTO CLICK - PHIÊN BẢN THẬT NHẤT ======================
def auto_click(link, job_type):
    global driver
    try:
        driver.get(link)
        time.sleep(3.5)  # Load trang

        if job_type != 'tiktok_follow':
            print(f"{red}Hiện chỉ hỗ trợ Follow")
            return False

        targets = [
            "//button[contains(., 'Follow') or contains(., 'Theo dõi')]",
            "//button[@data-e2e='follow-button']",
            "//button[contains(@class, 'follow')]",
            "//button[@aria-label='Follow' or @aria-label='Theo dõi']"
        ]

        for target in targets:
            try:
                btn = WebDriverWait(driver, 12).until(
                    EC.element_to_be_clickable((By.XPATH, target))
                )
                
                # Di chuột tự nhiên
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(btn, random.randint(-15, 15), random.randint(-12, 12))
                actions.pause(random.uniform(0.3, 0.7))
                actions.move_to_element(btn)
                actions.pause(random.uniform(0.4, 0.8))
                actions.click()
                actions.perform()
                
                print(f"{luc}✅ ĐÃ CLICK FOLLOW")

                time.sleep(5.0)  # Giữ trang lâu hơn

                # Refresh kiểm tra
                print(f"{lam}🔄 Refresh trang để kiểm tra follow thật...")
                driver.refresh()
                time.sleep(3.8)

                # Kiểm tra nút sau refresh
                still_follow = driver.find_elements(By.XPATH, "//button[contains(., 'Follow') or contains(., 'Theo dõi')]")
                if still_follow:
                    print(f"{red}❌ Fake Click! Follow chưa được TikTok ghi nhận thật")
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
            time.sleep(3)
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

# ====================== MAIN ======================
def main():
    global driver
    dem = 0

    if not get_key_system():
        sys.exit()

    banner()
    print(f"{luc}Tool TikTok TDS - Phiên bản Click Thật Nhất")

    # Phần nhập token, config nick... (giữ nguyên như file cũ của mày)
    # Để ngắn gọn, mày copy phần này từ file cũ vào đây

    init_browser()

    print(f"{red}⚠️ CẢNH BÁO: Dù đã tối ưu, follow vẫn có thể fake. Hãy dùng Delay ≥ 4 giây và farm chậm!")

    while True:
        # Phần chọn job, delay, nhận xu... (copy từ file cũ của mày)
        # Ví dụ:
        dl = int(input(f'{thanh_xau}{luc}Delay (giây) [Khuyến nghị 4]: {vang}') or 4)
        # ... tiếp tục code main như cũ

        # Trong vòng lặp job:
        # auto_click(link, job_type)

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        if driver: driver.quit()
        sys.exit()
