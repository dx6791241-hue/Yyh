import requests
import json
import time
import random
import mimetypes
import re, base64
import os, sys
import uuid
from datetime import datetime, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor # Thư viện cần cho main_get_key
from typing import Dict, Any, Optional

# ================== 1. GIAO DIỆN & BANNER ==================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ban = r"""
                        ___                                                       ,--.'|        
   ,--,  | :                       ,--.'|_                           ,---.,--,    :  : |        
,---.'|  : '                       |  | :,'   ,---.     __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                       :  : ' :  '    ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |    ,---.      ,---. .;__,'  /  /    /   |'  | |' |/___/ \  | |:   :  \ | :        
|   ' '  ; :   /     \    /     \|  |   |  .    ; ,. :|  |   ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. |  /    /  |  /    / ':__,'| :  '    | |: :'  :  /   \   \  \: |'   ' ;.    ;        
|   | :  | '.    ' / |.    ' /    '  : |__'    | .; :|  | '      ;   \  ' .|   | | \   |        
'   : |  : ;'    ;   /|'    ; :__  |  | '.'|    :    |;  : |       \   \   ''   :|  ; .'        
|   | '  ,/ '    |  / |'    | '.'| ;  :    ;\    \  / |  , ;        \   `  ;|   | '`--'          
;   : ;--'  |    :   ||    :    : |  ,    /  `----'   ---'          :   \ |'   : |              
|   ,/        \    \  /  \    \  /   ---`-'                          '---" ;   |.'              
'---'          `----'    `----'                                          '---'
"""
    for char in ban:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.002)

# ================== 2. CÁC HÀM HỖ TRỢ (KEY, IP, MÃ HÓA) ==================
def encrypt_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def decrypt_data(data: str) -> str:
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}")
    else:
        print("Không thể lấy địa chỉ IP của thiết bị.")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
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

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link_phu(url):
    try:
        token = "6989d7bcd70a74263103abab"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": "Không thể kết nối dịch vụ rút gọn."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi: {e}"}

def main_get_key():
    ip_address = get_ip_address()
    display_ip_address(ip_address)
    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn, mời bạn dùng tool...")
            time.sleep(2)
        else:
            if da_qua_gio_moi():
                print("\033[1;33mQuá giờ sử dụng tool !!!")
                sys.exit()
            url, key, expiration_date = generate_key_and_url(ip_address)
            with ThreadPoolExecutor(max_workers=2) as executor:
                print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mNhập 1 Để Lấy Key \033[1;33m( Free )")
                while True:
                    choice = input("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;34mNhập lựa chọn: ")
                    print("\033[97m════════════════════════════════════════════════")
                    if choice == "1":
                        yeumoney_data = executor.submit(get_shortened_link_phu, url).result()
                        if yeumoney_data.get('status') == "error":
                            print(yeumoney_data.get('message'))
                            sys.exit()
                        link_key = yeumoney_data.get('shortenedUrl')
                        print('\033[1;35mLink Để Vượt Key:', link_key)
                        ADMIN_KEY = "hectoradminskibidi123"
                        while True:
                            keynhap = input('\033[1;33mKey Đã Vượt Là: ').strip()
                            if keynhap == key or keynhap == ADMIN_KEY:
                                print('\033[1;32mKey Đúng Mời Bạn Dùng Tool\033[0m')
                                sleep(2)
                                luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                return
                            else:
                                print('\033[1;31mKey Sai, Vượt Lại:\033[0m', link_key)

# ================== 3. CÁC CLASS XỬ LÝ FACEBOOK ==================
class CookieHandler:
    @staticmethod
    def to_dict(cookie_str: str) -> Dict[str, str]:
        return {k.strip(): v.strip() for item in cookie_str.split(";") 
                if "=" in item for k, v in [item.split("=", 1)]}

class NumberEncoder:
    @staticmethod
    def to_base36(num: int) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        if num == 0: return "0"
        result = ""
        while num:
            num, remainder = divmod(num, 36)
            result = chars[remainder] + result
        return result

class HTMLExtractor:
    @staticmethod
    def find_pattern(html: str, pattern: str) -> Optional[str]:
        match = re.search(pattern, html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_token(html: str) -> Optional[str]:
        patterns = [r'DTSGInitialData".*?"token":"([^"]+)"', r'"token":"([^"]+)"']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None
    
    @staticmethod
    def extract_lsd(html: str) -> Optional[str]:
        patterns = [r'LSD".*?"token":"([^"]+)"', r'"token":"([^"]+)"']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None
    
    @staticmethod
    def extract_user_id(html: str) -> Optional[str]:
        patterns = [r'"actorID":"(\d+)"', r'"USER_ID":"(\d+)"', r'c_user=(\d+)']
        for pattern in patterns:
            result = HTMLExtractor.find_pattern(html, pattern)
            if result: return result
        return None
    
    @staticmethod
    def extract_revision(html: str) -> Optional[str]:
        return HTMLExtractor.find_pattern(html, r'client_revision["\s:]+(\d+)')
    
    @staticmethod
    def extract_jazoest(html: str) -> Optional[str]:
        return HTMLExtractor.find_pattern(html, r'jazoest=(\d+)')

class FacebookSession:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.token = self.user_id = self.revision = self.jazoest = self.lsd = None
        
    def authenticate(self) -> bool:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get("https://www.facebook.com/", headers=headers, cookies=CookieHandler.to_dict(self.cookie), timeout=30)
            html = response.text
            self.token = HTMLExtractor.extract_token(html)
            self.user_id = HTMLExtractor.extract_user_id(html)
            self.revision = HTMLExtractor.extract_revision(html) or "1000000"
            self.jazoest = HTMLExtractor.extract_jazoest(html) or "0"
            self.lsd = HTMLExtractor.extract_lsd(html) or "0"
            return True if self.user_id else False
        except Exception:
            return False

class GenData:
    def __init__(self, session: FacebookSession):
        self.session = session
        self.request_counter = 0
    
    def build_REACTION(self, reaction: str, ID_POST: str, doc_id='24198888476452283') -> Dict[str, Any]:
        self.request_counter += 1   
        reaction_id_list = {'LIKE':1635855486666999, 'LOVE':1678524932434102, 'CARE':613557422527858, 'HAHA':115940658764963, 'WOW':478547315650144, 'SAD':908563459236466, 'ANGRY':444813342392137}
        reaction_id_ = reaction_id_list.get(reaction, 'ERR')
        if reaction_id_ == "ERR": return {'err': 'Không Thể Sử Dụng Loại Cảm Xúc Này'}
        
        idpost = base64.b64encode(f"feedback:{ID_POST}".encode("utf-8")).decode("utf-8")
        return {
            'av': self.session.user_id, '__user': self.session.user_id,
            '__req': NumberEncoder.to_base36(self.request_counter), '__rev': self.session.revision,
            'fb_dtsg': self.session.token, 'jazoest': self.session.jazoest, 'lsd': self.session.lsd,
            'variables': '{"input":{"feedback_id":"'+idpost+'","feedback_reaction_id":"'+str(reaction_id_)+'","session_id":"'+str(uuid.uuid4())+'","actor_id":"'+self.session.user_id+'","client_mutation_id":"1"}}',
            'doc_id': doc_id,
        }

    def build_CMT(self, cmt: str, ID_POST: str, Group_id: str, doc_id='24615176934823390') -> Dict[str, Any]:
        self.request_counter += 1
        idpost = base64.b64encode(f"feedback:{ID_POST}".encode("utf-8")).decode("utf-8")
        return {
           'av': self.session.user_id, '__user': self.session.user_id,
           '__req': NumberEncoder.to_base36(self.request_counter), '__rev': self.session.revision,
           'fb_dtsg': self.session.token, 'jazoest': self.session.jazoest, 'lsd': self.session.lsd,
           'variables': '{"groupID":'+Group_id+',"input":{"message":{"text":"'+cmt+'"},"feedback_id":"'+idpost+'","idempotence_token":"client:'+str(uuid.uuid4())+'","actor_id":"'+self.session.user_id+'"}}',
           'doc_id': doc_id,
        }

class FB_API:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.session = FacebookSession(cookie)
        self.ready = False
        
    def login(self) -> bool:
        if self.session.authenticate():
            self.payload_builder = GenData(self.session)
            self.ready = True
            self.header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "cookie": self.cookie, "x-fb-lsd": self.session.lsd
            }
            return True
        return False
        
    def REACTION(self, REACTION: str, Id_post: str):
        if not self.ready and not self.login(): return {"error": "Not logged in"}
        payload = self.payload_builder.build_REACTION(REACTION, Id_post)
        if 'err' in payload: return payload
        res = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload)
        return res.json()

    def CMT(self, cmt: str, Id_post: str, Group_id='null'):
        if not self.ready and not self.login(): return {"error": "Not logged in"}
        payload = self.payload_builder.build_CMT(cmt, Id_post, Group_id)
        res = requests.post('https://www.facebook.com/api/graphql/', headers=self.header, data=payload)
        return res.json()

# ================== 4. KHỐI CHẠY CHÍNH CỦA TOOL ==================
if __name__ == "__main__":
    # Chạy hàm get key (sẽ tự động gọi display_ip_address và hiện banner)
    main_get_key()

    print("\n\033[1;36mDev: Deltatrash09 (Duong Khoi)")
    print("SDT: 0949557645\033[0m\n")

    # --- MENU FACEBOOK ---
    cookie = input("\033[1;97mNhập Cookie Facebook của bạn: ").strip()
    fb = FB_API(cookie)

    print("\nChọn chức năng:")
    # --- MENU FACEBOOK ---
    cookie = input("\n\033[1;97mNhập Cookie Facebook của bạn: ").strip()
    fb = FB_API(cookie)

    while True:
        print("\n\033[1;36m" + "="*30)
        print("CHỌN CHỨC NĂNG:")
        print("1. Reaction")
        print("2. Comment Spam (Có chống Block)")
        print("3. Thoát Tool")
        print("="*30 + "\033[0m")
        
        # Dùng .strip() để lỡ gõ dư dấu cách tool vẫn nhận được
        choice = input("\033[1;97mChọn (1/2/3): ").strip()

        if choice == '1':
            id_p = input("ID bài viết: ").strip()
            react = input("Loại (LIKE, LOVE...): ").upper().strip()
            print(fb.REACTION(react, id_p))
            
        elif choice == '2':
            id_p = input("ID bài viết: ").strip()
            
            print("\033[1;33mMẹo: Nhập nhiều nội dung cách nhau bằng dấu '|' để random thay đổi câu liên tục.")
            print("Ví dụ: Tuyệt vời quá|Lên top nha|Xin chào mọi người\033[0m")
            nd_input = input("Nội dung spam: ")
            danh_sach_nd = nd_input.split('|') # Tách các câu ra thành danh sách
            
            gr_id = input("ID Group (Enter nếu không có): ").strip() or 'null'
            
            try:
                lần = int(input("Số lần spam: "))
                nghỉ = int(input("Delay (giây - Khuyên dùng > 10s): ") or 10)
                print("\n\033[1;32mBẮT ĐẦU SPAM...\033[0m")
                for i in range(lần):
                    # Bốc ngẫu nhiên 1 câu trong danh sách để gửi
                    nd_spam = random.choice(danh_sach_nd).strip()
                    print(f"[Lần {i+1}] Đang gửi: '{nd_spam}' ...", end=" ")
                    
                    print(fb.CMT(nd_spam, id_p, gr_id))
                    
                    if i < lần - 1: 
                        time.sleep(nghỉ)
                print("\033[1;32mHoàn thành đợt Spam!\033[0m")
            except ValueError:
                print("\033[1;31mLỗi: Bạn phải nhập số cho số lần và delay!\033[0m")
                
        elif choice == '3':
            print("\033[1;32mCảm ơn bạn đã sử dụng tool. Tạm biệt!\033[0m")
            break # Thoát vòng lặp, tắt tool
            
        else:
            print("\033[1;31mLựa chọn không hợp lệ, vui lòng gõ đúng 1, 2 hoặc 3!\033[0m")