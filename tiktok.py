# -*- coding: utf-8 -*-
import requests
import os
import sys
import time
import shutil
import random
from sys import platform
from datetime import datetime

# ================== MÀU SẮC ==================
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lam = "\033[1;36m"

thanh_xau = red + "[" + trang + "=.=" + red + "] " + trang + "=> "

# ================== SELENIUM ==================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

total = 0
may = 'mb' if platform[0:3] == 'lin' else 'pc'

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    ban = f"""
                                                                         
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
"""
    for char in ban:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.001)

class TraoDoiSub:
    def __init__(self, token):
        self.token = token
        self.base = "https://traodoisub.com/api/"

    def profile(self):
        try:
            r = requests.get(f"{self.base}?fields=profile&access_token={self.token}", timeout=10)
            return r.json().get('data')
        except:
            return None

    def set_tiktok_run(self, tiktok_id):
        try:
            url = f"{self.base}?fields=tiktok_run&id={tiktok_id}&access_token={self.token}"
            return requests.get(url, timeout=10).json()
        except:
            return None

    def get_job(self, job_type):
        try:
            url = f"{self.base}?fields={job_type}&access_token={self.token}"
            return requests.get(url, timeout=10)
        except:
            return None

    def cache(self, job_id, cache_type):
        try:
            url = f"{self.base}coin/?type={cache_type}&id={job_id}&access_token={self.token}"
            r = requests.get(url, timeout=10)
            return "success" in r.text.lower() or "cache" in r.text.lower()
        except:
            return False

    def nhan_xu(self, nhan_type):
        global total
        try:
            url = f"{self.base}coin/?type={nhan_type}&id={nhan_type}_API&access_token={self.token}"
            data = requests.get(url, timeout=10).json()
            if 'data' in data:
                xuthem = data['data'].get('xu_them', 0)
                xu_hien_tai = data['data'].get('xu', 0)
                total += int(xuthem)
                print(f'\n{lam}Nhận Thành Công {red}| {luc}Cộng: {vang}{xuthem} {luc}Xu {red}| {luc}Tổng: {vang}{total} {luc}Xu {red}| {vang}{xu_hien_tai}')
                return True
            return False
        except:
            return False

def init_browser():
    chrome_options = Options()
    profile_dir = "ChromeProfileTDS" if may == "pc" else "./ChromeProfileTDS"

    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")

    try:
        print(f"{luc}Đang khởi tạo browser...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_page_load_timeout(60)
        print(f"{luc}✅ Browser đã mở thành công!")
        return driver
    except Exception as e:
        print(f"{red}❌ Không mở được browser: {e}")
        if os.path.exists(profile_dir):
            print(f"{vang}Đang xóa thư mục profile cũ: {profile_dir}")
            try:
                shutil.rmtree(profile_dir)
                print(f"{luc}Đã xóa profile. Đang thử lại...")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.set_page_load_timeout(60)
                print(f"{luc}✅ Browser đã mở thành công sau khi xóa profile!")
                return driver
            except Exception as e2:
                print(f"{red}Vẫn lỗi sau khi xóa profile: {e2}")
        print(f"{vang}Hướng dẫn: Đóng hết Chrome đang chạy và thử lại.")
        input("Nhấn Enter để thoát...")
        sys.exit()

def click_follow(driver):
    follow_xpaths = [
        "//button[contains(text(), 'Follow') or contains(text(), 'Theo dõi')]",
        "//div[@data-e2e='follow-button']//button",
        "//button[@data-e2e='follow-button']",
        "//button[contains(@class, 'follow')]"
    ]

    def is_follow_button_present():
        for xp in follow_xpaths:
            try:
                btn = driver.find_element(By.XPATH, xp)
                if btn.is_displayed():
                    return True
            except:
                continue
        return False

    # Thử click tối đa 2 lần
    for attempt in range(2):
        clicked = False
        for xp in follow_xpaths:
            try:
                btn = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                print(f"{luc}✅ Đã click Follow! (lần {attempt+1})")
                clicked = True
                break
            except:
                continue
        if not clicked:
            print(f"{red}❌ Không tìm thấy nút follow")
            return False

        time.sleep(2)
        driver.refresh()
        time.sleep(4)

        if not is_follow_button_present():
            print(f"{luc}✅ Follow thành công!")
            return True
        else:
            print(f"{vang}⚠️ Lần {attempt+1}: sau refresh vẫn còn nút Follow, thử lại sau {5*(attempt+1)}s")
            time.sleep(5 * (attempt + 1))

    print(f"{red}❌ Follow thất bại sau 2 lần thử")
    return False

def click_like(driver):
    like_xpaths = [
        "//button[@data-e2e='like-icon']",
        "//button[contains(@aria-label, 'Like') or contains(@aria-label, 'Thích')]"
    ]
    for xp in like_xpaths:
        try:
            btn = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, xp)))
            driver.execute_script("arguments[0].click();", btn)
            print(f"{luc}✅ Đã click Like!")
            time.sleep(2)
            return True
        except:
            continue
    print(f"{red}❌ Không tìm thấy nút like")
    return False

def click_comment(driver):
    try:
        comment_icon_xpaths = [
            "//button[@data-e2e='comment-icon']",
            "//button[contains(@aria-label, 'Comment') or contains(@aria-label, 'Bình luận')]"
        ]
        for xp in comment_icon_xpaths:
            try:
                comment_btn = WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", comment_btn)
                break
            except:
                continue
        else:
            print(f"{red}❌ Không tìm thấy nút comment")
            return False

        time.sleep(2)

        input_xpaths = [
            "//div[@contenteditable='true']",
            "//div[@data-e2e='comment-input']//div[@contenteditable='true']",
            "//textarea[contains(@placeholder, 'Bình luận')]"
        ]
        cmt = "Hay quá! ❤️"
        for xp in input_xpaths:
            try:
                comment_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xp)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_input)
                driver.execute_script("arguments[0].focus();", comment_input)
                comment_input.send_keys(cmt)
                time.sleep(1)
                break
            except:
                continue

        send_xpaths = [
            "//button[contains(text(), 'Send') or contains(text(), 'Gửi')]",
            "//button[@data-e2e='comment-post-button']"
        ]
        for xp in send_xpaths:
            try:
                send_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", send_btn)
                print(f"{luc}✅ Đã comment: {cmt}")
                time.sleep(2)
                return True
            except:
                continue
        print(f"{red}❌ Không gửi được comment")
        return False
    except Exception as e:
        print(f"{red}⚠️ Lỗi auto comment: {e}")
        return False

def auto_click(driver, link, job_type):
    try:
        print(f"{luc}Mở link: {trang}{link[:50]}...")
        driver.get(link)
        # Chờ 4 giây để trang load cơ bản
        time.sleep(4)

        if job_type == 'tiktok_follow':
            return click_follow(driver)
        elif job_type == 'tiktok_like':
            return click_like(driver)
        elif job_type == 'tiktok_comment':
            return click_comment(driver)
        else:
            return False
    except Exception as e:
        print(f"{red}⚠️ Lỗi khi xử lý job: {e}")
        return False

def main():
    global total
    dem = 0          # Số job đã xử lý (thành công hay không)
    success_dem = 0  # Số job thành công
    fail_count = 0   # Số lần thất bại liên tiếp
    max_fail = 5

    banner()

    # ================== ĐĂNG NHẬP TDS ==================
    while True:
        if os.path.exists('configtds.txt'):
            with open('configtds.txt', 'r', encoding='utf-8') as f:
                token = f.read().strip()
        else:
            token = input(f'{thanh_xau}{luc}Nhập Access Token TDS: {vang}').strip()
            with open('configtds.txt', 'w', encoding='utf-8') as f:
                f.write(token)

        tds = TraoDoiSub(token)
        data = tds.profile()
        if data:
            user = data.get('user', 'Unknown')
            xu = data.get('xu', 0)
            print(f"{luc}Đăng nhập TDS thành công! → {vang}{user}")
            break
        else:
            print(f"{red}Token sai hoặc hết hạn!")
            if os.path.exists('configtds.txt'):
                os.remove('configtds.txt')

    # ================== CẤU HÌNH TIKTOK ID ==================
    tiktok_id = input(f'{thanh_xau}{luc}Nhập ID TikTok muốn chạy: {vang}').strip()
    res_set = tds.set_tiktok_run(tiktok_id)
    if res_set and 'success' in str(res_set).lower():
        print(f'{luc}✅ Đã cấu hình nick {vang}{tiktok_id}{luc} thành công!')
    else:
        print(f'{red}❌ Cấu hình nick TikTok thất bại!')
        return

    driver = init_browser()

    # ================== CHẾ ĐỘ CHẠY ==================
    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Tim (Like) | 2 → Follow | 3 → Comment')
        nhiem_vu = input(f'{thanh_xau}{luc}Chọn: {vang}').strip()
        dl_input = input(f'{thanh_xau}{luc}Delay (giây, mặc định random 5-12): {vang}').strip()
        if dl_input:
            dl = int(dl_input)
        else:
            dl = None
        nv_nhan = int(input(f'{thanh_xau}{luc}Nhận xu sau bao nhiêu job thành công: {vang}'))

        if nhiem_vu == '1':
            job_type, cache_type, nhan_type = 'tiktok_like', 'TIKTOK_LIKE_CACHE', 'TIKTOK_LIKE'
        elif nhiem_vu == '2':
            job_type, cache_type, nhan_type = 'tiktok_follow', 'TIKTOK_FOLLOW_CACHE', 'TIKTOK_FOLLOW'
        elif nhiem_vu == '3':
            job_type, cache_type, nhan_type = 'tiktok_comment', 'TIKTOK_COMMENT_CACHE', 'TIKTOK_COMMENT'
        else:
            print(f"{red}Lựa chọn không hợp lệ!")
            continue

        print(f"{luc}Đang chạy job {job_type.upper()}... (Nhấn Ctrl + C để dừng)")

        while True:
            listjob = tds.get_job(job_type)
            try:
                jobs = listjob.json().get('data', []) if listjob else []
            except:
                jobs = []

            if not jobs:
                print(f"{red}Hết job, đang chờ 10 giây...", end='\r')
                time.sleep(10)
                continue

            for job in jobs:
                job_id = job.get('id')
                link = job.get('link')

                print(f"{vang}[{dem+1}] {luc}Đang làm job: {trang}{job_id}")

                success = auto_click(driver, link, job_type)
                dem += 1
                if success:
                    success_dem += 1
                    fail_count = 0
                else:
                    fail_count += 1
                    if fail_count >= max_fail:
                        print(f"{red}⚠️ Thất bại {max_fail} lần liên tiếp. Có thể tài khoản bị giới hạn. Dừng 60 giây...")
                        time.sleep(60)
                        fail_count = 0

                if success and tds.cache(job_id, cache_type):
                    tg = datetime.now().strftime('%H:%M:%S')
                    print(f'{luc}[{dem}] {red}| {lam}{tg} {red}| {luc}CACHE THÀNH CÔNG {red}| {trang}{job_id}')
                    # Delay ngẫu nhiên nếu không nhập
                    if dl is None:
                        delay = random.randint(5, 12)
                    else:
                        delay = dl
                    time.sleep(delay)

                    if success_dem % nv_nhan == 0 and success_dem > 0:
                        print(f"{luc}Đạt {success_dem} job thành công, tiến hành nhận xu...")
                        tds.nhan_xu(nhan_type)
                else:
                    print(f"{red}Lỗi cache job ID: {job_id}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red}Đã dừng chương trình!")
        sys.exit()
    except Exception as e:
        print(f"{red}Lỗi không xác định: {e}")
