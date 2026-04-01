# -*- coding: utf-8 -*-
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lam = "\033[1;36m"

thanh_xau = red + "[" + trang + "=.=" + red + "] " + trang + "=> "

import requests, os, sys, time
from sys import platform
from datetime import datetime

# ================== SELENIUM IMPORT MỚI ==================
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
        time.sleep(0.00125)

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
                print(f'\n{lam}Nhận Thành Công {red}| {luc}Cộng: {vang}{xuthem} {luc}Xu {red}| {luc}Tổng: {vang}{total} {luc}Xu {red}| {vang}{xu_hien_tai}')
                return True
            return False
        except: return False

def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=C:\\ChromeProfileTDS")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# ================== HÀM TỰ CLICK ĐÃ SỬA (LIKE - FOLLOW - COMMENT) ==================
def auto_click(driver, link, job_type):
    try:
        driver.get(link)
        time.sleep(8)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
        except:
            pass

        if job_type == 'tiktok_like':
            targets = [
                "//button[@data-e2e='like-icon']",
                "//button[contains(@aria-label, 'Like') or contains(@aria-label, 'Thích')]",
                "//div[contains(@class, 'like')]//button"
            ]
        elif job_type == 'tiktok_follow':
            targets = [
                "//button[contains(text(), 'Follow') or contains(text(), 'Theo dõi')]",
                "//div[@data-e2e='follow-button']//button",
                "//button[@data-e2e='follow-button']",
                "//div[contains(@data-e2e, 'follow')]//button"
            ]
        elif job_type == 'tiktok_comment':
            return auto_comment(driver)
        else:
            targets = []

        for target in targets:
            try:
                btn = WebDriverWait(driver, 12).until(
                    EC.element_to_be_clickable((By.XPATH, target))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                print(f"{luc}✅ Đã click thành công {job_type.upper()} | XPath: {target}")
                time.sleep(3)
                return True
            except:
                continue

        print(f"{red}❌ Không tìm thấy nút {job_type} trên trang này.")
        return False

    except Exception as e:
        print(f"{red}⚠️ Lỗi trình duyệt: {e}")
        return False


def auto_comment(driver):
    try:
        comment_icon_xpaths = [
            "//button[@data-e2e='comment-icon']",
            "//div[@data-e2e='comment-icon']//button",
            "//button[contains(@aria-label, 'Comment') or contains(@aria-label, 'Bình luận')]"
        ]
        
        comment_btn = None
        for xp in comment_icon_xpaths:
            try:
                comment_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xp))
                )
                break
            except:
                continue

        if not comment_btn:
            print(f"{red}❌ Không tìm thấy nút comment")
            return False

        driver.execute_script("arguments[0].click();", comment_btn)
        print(f"{luc}✅ Đã mở hộp comment")
        time.sleep(3)

        input_xpaths = [
            "//div[@contenteditable='true' and contains(@class, 'DraftEditor')]",
            "//div[@data-e2e='comment-input']//div[@contenteditable='true']",
            "//div[contains(@class, 'comment-input')]//div[@contenteditable]",
            "//textarea[contains(@placeholder, 'Bình luận') or contains(@placeholder, 'Comment')]"
        ]

        comment_input = None
        for xp in input_xpaths:
            try:
                comment_input = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, xp))
                )
                break
            except:
                continue

        if comment_input:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_input)
            driver.execute_script("arguments[0].focus();", comment_input)
            
            cmt = "Hay lắm ❤️"   # Bạn có thể thay câu comment khác ở đây
            comment_input.send_keys(cmt)
            time.sleep(1.5)

            send_xpaths = [
                "//button[contains(text(), 'Send') or contains(text(), 'Gửi')]",
                "//button[@data-e2e='comment-post-button']",
                "//div[contains(@class, 'send')]//button"
            ]
            for xp in send_xpaths:
                try:
                    send_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xp))
                    )
                    driver.execute_script("arguments[0].click();", send_btn)
                    print(f"{luc}✅ Đã comment: {cmt}")
                    time.sleep(3)
                    return True
                except:
                    continue

        print(f"{red}❌ Không tìm thấy ô nhập comment")
        return False

    except Exception as e:
        print(f"{red}⚠️ Lỗi auto comment: {e}")
        return False


def main():
    global total
    dem = 0
    banner()

    # Login
    while True:
        if os.path.exists('configtds.txt'):
            with open('configtds.txt', 'r') as f: token = f.read().strip()
        else:
            token = input(f'{thanh_xau}{luc}Nhập Access Token TDS: {vang}')
            with open('configtds.txt', 'w') as f: f.write(token)

        tds = TraoDoiSub(token)
        data = tds.profile()
        if data:
            print(lam + ' Đăng nhập TDS thành công!')
            user, xu = data.get('user'), data.get('xu')
            break
        else:
            print(red + 'Token sai!'); os.remove('configtds.txt') if os.path.exists('configtds.txt') else None

    # Config TikTok ID
    tiktok_id = input(f'{thanh_xau}{luc}Nhập ID TikTok muốn chạy: {vang}').strip()
    res_set = tds.set_tiktok_run(tiktok_id)
    if res_set and 'success' in str(res_set):
        print(f'{luc}✅ Đã cấu hình nick {vang}{tiktok_id}{luc} thành công!')
    else:
        print(red + '❌ Cấu hình nick thất bại!'); return

    driver = init_browser()

    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Tim (Like) | 2 → Follow | 3 → Comment')
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
                print(red + 'Hết job, đang chờ...', end='\r'); time.sleep(10); continue

            for job in jobs:
                job_id, link = job['id'], job['link']
                auto_click(driver, link, job_type)   # ← ĐÃ SỬA Ở ĐÂY
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
    try: main()
    except KeyboardInterrupt: sys.exit()
