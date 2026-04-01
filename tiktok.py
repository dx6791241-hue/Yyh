# -*- coding: utf-8 -*-
import requests, os, sys, time
from datetime import datetime

# ================== MÀU SẮC ==================
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
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

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
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
""")

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

# ================== INIT BROWSER ==================
def init_browser():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=ChromeProfileTDS")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        print(f"{luc}✅ Browser đã mở thành công (Profile được giữ nguyên)")
        return driver
    except Exception as e:
        print(f"{red}❌ Lỗi mở browser: {e}")
        sys.exit()

# ================== AUTO CLICK - PHIÊN BẢN MẠNH HƠN ==================
def auto_click(driver, link, job_type):
    try:
        print(f"{luc}Đang mở link: {trang}{link[:70]}...")
        driver.set_page_load_timeout(40)   # Ngăn kẹt vô thời hạn
        driver.get(link)
        time.sleep(10)                     # Tăng thời gian chờ load TikTok

        if job_type == 'tiktok_follow':
            print(f"{luc}Đang thử click Follow ngay...")
            
            follow_xpaths = [
                "//button[contains(text(), 'Follow') or contains(text(), 'Theo dõi')]",
                "//div[@data-e2e='follow-button']//button",
                "//button[@data-e2e='follow-button']",
                "//button[contains(@class, 'follow')]"
            ]

            clicked = False
            for i, xp in enumerate(follow_xpaths, 1):
                try:
                    print(f"{lam}  Thử XPath {i}...")
                    btn = WebDriverWait(driver, 12).until(
                        EC.element_to_be_clickable((By.XPATH, xp))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    driver.execute_script("arguments[0].click();", btn)
                    print(f"{luc}✅ Đã click Follow thành công!")
                    clicked = True
                    time.sleep(4)
                    break
                except:
                    continue

            if not clicked:
                print(f"{red}❌ Không click được bằng XPath, thử JavaScript...")
                try:
                    driver.execute_script("""
                        let btns = document.querySelectorAll('button');
                        for (let b of btns) {
                            if (b.innerText && (b.innerText.includes('Follow') || b.innerText.includes('Theo dõi'))) {
                                b.scrollIntoView({block: 'center'});
                                b.click();
                                return true;
                            }
                        }
                    """)
                    print(f"{luc}✅ Đã click Follow bằng JavaScript!")
                    time.sleep(4)
                except:
                    print(f"{red}❌ JavaScript cũng không click được")

            # Kiểm tra sau refresh
            print(f"{luc}Đang refresh để kiểm tra...")
            driver.refresh()
            time.sleep(7)

            still_show = False
            for xp in follow_xpaths:
                try:
                    WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xp)))
                    still_show = True
                    break
                except:
                    continue

            if still_show:
                print(f"{vang}⚠️ Sau refresh vẫn còn nút Follow → Có thể chưa follow được")
            else:
                print(f"{luc}✅ Có vẻ đã Follow thành công!")

            return True

        # Like và Comment giữ nguyên
        elif job_type == 'tiktok_like':
            targets = [
                "//button[@data-e2e='like-icon']",
                "//button[contains(@aria-label, 'Like') or contains(@aria-label, 'Thích')]"
            ]
        elif job_type == 'tiktok_comment':
            return auto_comment(driver)
        else:
            targets = []

        for target in targets:
            try:
                btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, target)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                print(f"{luc}✅ Đã click {job_type.upper()} thành công")
                time.sleep(3)
                return True
            except:
                continue

        print(f"{red}❌ Không tìm thấy nút {job_type}")
        return False

    except Exception as e:
        print(f"{red}⚠️ Lỗi khi xử lý job: {e}")
        return False


def auto_comment(driver):
    try:
        comment_icon_xpaths = [
            "//button[@data-e2e='comment-icon']",
            "//button[contains(@aria-label, 'Comment') or contains(@aria-label, 'Bình luận')]"
        ]
        
        for xp in comment_icon_xpaths:
            try:
                comment_btn = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", comment_btn)
                print(f"{luc}✅ Đã mở hộp bình luận")
                break
            except:
                continue
        else:
            print(f"{red}❌ Không tìm thấy nút comment")
            return False

        time.sleep(3)

        input_xpaths = [
            "//div[@contenteditable='true']",
            "//textarea[contains(@placeholder, 'Bình luận')]"
        ]

        for xp in input_xpaths:
            try:
                comment_input = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xp)))
                driver.execute_script("arguments[0].focus();", comment_input)
                comment_input.send_keys("Hay lắm ❤️")
                time.sleep(1.5)
                break
            except:
                continue

        send_xpaths = ["//button[contains(text(), 'Send') or contains(text(), 'Gửi')]"]
        for xp in send_xpaths:
            try:
                send_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.execute_script("arguments[0].click();", send_btn)
                print(f"{luc}✅ Đã comment: Hay lắm ❤️")
                time.sleep(3)
                return True
            except:
                continue
        return False
    except Exception as e:
        print(f"{red}⚠️ Lỗi comment: {e}")
        return False


def main():
    global total
    dem = 0
    banner()

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

    tiktok_id = input(f'{thanh_xau}{luc}Nhập ID TikTok muốn chạy: {vang}').strip()
    res_set = tds.set_tiktok_run(tiktok_id)
    if res_set and 'success' in str(res_set).lower():
        print(f'{luc}✅ Đã cấu hình nick {vang}{tiktok_id}{luc} thành công!')
    else:
        print(f'{red}❌ Cấu hình nick TikTok thất bại!')
        return

    driver = init_browser()

    while True:
        banner()
        print(f'{thanh_xau}{luc}Tên TK: {vang}{user} {red}| {luc}Xu: {vang}{xu}')
        print(f'{thanh_xau}{luc}1 → Like | 2 → Follow | 3 → Comment')
        nhiem_vu = input(f'{thanh_xau}{luc}Chọn: {vang}').strip()
        dl = int(input(f'{thanh_xau}{luc}Delay (giây): {vang}'))
        nv_nhan = int(input(f'{thanh_xau}{luc}Nhận xu sau bao nhiêu job: {vang}'))

        if nhiem_vu == '1':
            job_type, cache_type, nhan_type = 'tiktok_like', 'TIKTOK_LIKE_CACHE', 'TIKTOK_LIKE'
        elif nhiem_vu == '2':
            job_type, cache_type, nhan_type = 'tiktok_follow', 'TIKTOK_FOLLOW_CACHE', 'TIKTOK_FOLLOW'
        elif nhiem_vu == '3':
            job_type, cache_type, nhan_type = 'tiktok_comment', 'TIKTOK_COMMENT_CACHE', 'TIKTOK_COMMENT'
        else:
            continue

        print(f"{luc}Đang chạy job {job_type.upper()}...")

        while True:
            listjob = tds.get_job(job_type)
            try:
                jobs = listjob.json().get('data', []) if listjob else []
            except:
                jobs = []

            if not jobs:
                print(f"{red}Hết job, chờ 10 giây...", end='\r')
                time.sleep(10)
                continue

            for job in jobs:
                job_id = job.get('id')
                link = job.get('link')
                
                print(f"{vang}[{dem+1}] {luc}Đang làm job: {trang}{job_id}")
                
                success = auto_click(driver, link, job_type)
                dem += 1

                if success and tds.cache(job_id, cache_type):
                    tg = datetime.now().strftime('%H:%M:%S')
                    print(f'{luc}[{dem}] {red}| {lam}{tg} {red}| {luc}CACHE THÀNH CÔNG {red}| {trang}{job_id}')
                    time.sleep(dl)
                    if dem % nv_nhan == 0:
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
