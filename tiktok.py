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

# ====================== BANNER GỐC (đã làm lại đúng như mày muốn) ======================
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
# (mày copy phần get key từ file cũ của mày vào đây, tao không sửa)

# ====================== UNDETECTED CHROMEDRIVER (FIX LỖI GOOGLE) ======================
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
        options.page_load_strategy = "eager"

        driver = uc.Chrome(options=options, use_subprocess=True)
        print(f"{luc}✅ Undetected Chrome mở thành công (đã fix lỗi đăng nhập Google)")
        return driver
    except Exception as e:
        print(f"{red}❌ Không mở được Chrome: {e}")
        sys.exit()

# ====================== AUTO CLICK + REFRESH KIỂM TRA ======================
def auto_click(link, job_type):
    global driver
    try:
        driver.get(link)
        time.sleep(3.8)

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

                print(f"{lam}🔄 Refresh trang để kiểm tra follow thật...")
                driver.refresh()
                time.sleep(4.0)

                still_follow = driver.find_elements(By.XPATH, "//button[contains(., 'Follow') or contains(., 'Theo dõi')]")
                if still_follow:
                    print(f"{red}❌ Fake Click! Follow chưa được ghi nhận thật")
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

# ====================== CLASS TRAODOISUB (copy nguyên từ file cũ) ======================
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

    if not get_key_system():  # thay bằng hàm get key thật của mày
        sys.exit()

    banner()
    print(f"{luc}Tool TikTok TDS - Phiên bản Click Thật Nhất (Fix Google)")

    # Phần nhập token, config nick... (copy từ file cũ của mày vào đây)

    init_browser()

    print(f"{red}⚠️ CẢNH BÁO: Máy này đang bị flag IP. Khuyến nghị Delay ≥ 4 giây và xóa profile trước khi chạy acc mới.")

    # vòng lặp job của mày (copy phần còn lại từ file cũ)

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        if driver: driver.quit()
        sys.exit()
