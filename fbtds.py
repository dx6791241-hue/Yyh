import hashlib, random, requests, time, os, sys, json, re, base64, uuid
from time import sleep
from random import randint
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

red = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
tim = "\033[1;35m"
lam = "\033[1;36m"
v = "\033[38;2;220;200;255m"
thanh = f'{red}[{trang}</>{red}] {trang}=>'
listnv = []
listck = []

def rgb(r, g, b): 
    return f"\033[38;2;{r};{g};{b}m"

def read_proxy_file(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []
    
def thanhngang(so):
    for i in range(so):
        print(trang + '-', end='')
    print('')

# =====================================================================
#  HÀM TẠO MÀU GRADIENT ĐỒNG BỘ 100% TỪ FBTTC.PY SANG
# =====================================================================
def gradient_3(text):
    def rgb_to_ansi(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    start, end = (0, 255, 0), (0, 128, 255) # Xanh lá -> Xanh biển
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

def gradient_2(text):
    def rgb_to_ansi(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    start_color, mid_color, end_color = (255, 87, 34), (255, 20, 147), (255, 255, 0) # Cam -> Hồng -> Vàng
    result = ""
    for i, char in enumerate(text):
        t = i / (len(text) - 1 if len(text) > 1 else 1)
        if t < 0.5:
            t2 = t / 0.5
            r = int(start_color[0] + (mid_color[0] - start_color[0]) * t2)
            g = int(start_color[1] + (mid_color[1] - start_color[1]) * t2)
            b = int(start_color[2] + (mid_color[2] - start_color[2]) * t2)
        else:
            t2 = (t - 0.5) / 0.5
            r = int(mid_color[0] + (end_color[0] - mid_color[0]) * t2)
            g = int(mid_color[1] + (end_color[1] - mid_color[1]) * t2)
            b = int(mid_color[2] + (end_color[2] - mid_color[2]) * t2)
        result += rgb_to_ansi(r, g, b) + char
    return result + "\033[0m"

# =====================================================================
# 🟩 KHU VỰC BANNER CHẠY GRADIENT ĐẸP KHÔNG LỖI
# =====================================================================
def banner():
    # Thêm chữ r sát đầu """ để Python hiểu là Raw String, né lỗi Syntax Windows
    my_banner_text = r"""
      ,--.'|                       ___                                         ,--.'|        
   ,--,  | :                     ,--.'|_                           ,---.   ,--,:  : |        
,---.'|  : '                     |  | :,'   ,---.    __  ,-.      /__./|,`--.'`|  ' :        
|   | : _' |                     :  : ' :  '   ,'\ ,' ,'/ /| ,---.;  ; ||   :  :  | |        
:   : |.'  |   ,---.     ,---. .;__,'  /  /   /   |'  | |' |/___/ \  | |:   |   \ | :        
|   ' '  ; :  /     \   /     \|  |    |  .   ; ,. :|  |  ,'\   ;  \ ' ||   : '  '; |        
'   |  .'. | /    /  | /    / ':__,'| :  '   | |: :'  :  /   \   \  \: |'   ' ;.   ;        
|   | :  | '.    ' / |.    ' /   '  : |__'   | .; :|  | '     ;   \  ' .|   | | \  |        
'   : |  : ;'    ;  /|'    ; :__ |  | '.'|   :    |;  : |      \   \   ''   : |  ; .'        
|   | '  ,/ '    |  / |'    | '.'| ;  :    ;\   \  / |  , ;       \   `  ;|   | '`--'          
;   : ;--'  |    :  | |    :    | |  ,    /  `----'   ---'         :   \ |'   : |              
|   ,/       \   \  /  \   \  /   ---`-'                            '---" ;   |.'              
'---'         `----'    `----'                                            '---'              
"""

    my_info_text = f"""
    ═══════════════════════════════════════════════════════════════════
    [+] Dev       : Deltatrash09 (Duong Khoi)
    [+] SDT       : 0949557645
    ═══════════════════════════════════════════════════════════════════
    """
    print(gradient_3(my_banner_text))
    print(gradient_2(my_info_text))

# =====================================================================

def Delay(value):
    total = value
    bar_len = 24  
    step = 0

    while value > 0:
        done = int(((total - value) / total) * bar_len)
        todo = bar_len - done

        bar = "["
        for i in range(bar_len):
            if i < done:
                t = (step + i) % 100 / 100
                r = int(160 + (0 - 160) * t)
                g = int(231 + (128 - 231) * t)
                b = int(229 + (255 - 229) * t)
                bar += f"{rgb(r, g, b)}#{'\033[0m'}"
            else:
                bar += "."
        bar += "]"

        print(bar, end='\r')
        sleep(0.1)
        value -= 0.1
        step += 3  

    print(" " * (bar_len + 10), end='\r')  


def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

class Facebook_Api(object):
    def __init__(self, cookie, proxy=None):
        try:
            self.lsd = ''
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.actor_id = self.cookie.split('c_user=')[1].split(';')[0]
            self.proxies = None
            self.headers = {
                'authority': 'www.facebook.com',
                'accept': '*/*',
                'cookie': self.cookie,
                'origin': 'https://www.facebook.com',
                'referer': 'https://www.facebook.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin'
            }
            if proxy:
                try:
                    proxy_parts = proxy.strip().split(':')
                    if len(proxy_parts) == 4:
                        host, port, user, password = proxy_parts
                        self.proxies = {
                            'http': f'http://{user}:{password}@{host}:{port}',
                            'https': f'http://{user}:{password}@{host}:{port}'
                        }
                except Exception as e:
                    print(f"Lỗi khởi tạo proxy: {str(e)}")
                    self.proxies = None
            url = requests.get(f'https://www.facebook.com/{self.actor_id}', headers=self.headers, proxies=self.proxies).url
            response = requests.get(url, headers=self.headers, proxies=self.proxies).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
                self.lsd += re.findall(r'\["LSD",\[\],\{"token":"(.*?)"\}', response)[0]
        except:
            pass
    
    def info(self):
        try:
            get = requests.get('https://www.facebook.com/me', headers=self.headers, proxies=self.proxies).text
            name = get.split('<title>')[1].split('</title>')[0]
            return {'success': 200, 'id': self.actor_id, 'name': name}
        except:
            return {'error': 200}
    
    def Checkspam(self):
        data = {
            "av": self.actor_id,
            "fb_dtsg": self.fb_dtsg,
            "jazoest": self.jazoest,
            "lsd": self.lsd,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "FBScrapingWarningMutation",
            "variables": "{}",
            "server_timestamps": "true",
            "doc_id": "6339492849481770"
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return response.text
        
    def reaction(self, id, type):
        reac = {
            "LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858",
            "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", "ANGRY": "444813342392137"
        }
        idreac = reac.get(type)
        data = {
            'av': self.actor_id,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': fr'{{"input":{{"feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{idreac}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"session_id":"{uuid.uuid4()}","actor_id":"{self.actor_id}"}}}}',
            'server_timestamps': 'true',
            'doc_id': '7047198228715224',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return '{"data":{"feedback_react":{"feedback":{"id":' in response.text
        
    def reactioncmt(self, id, type):
        reac = {
            "LIKE": "1635855486666999", "LOVE": "1678524932434102", "CARE": "613557422527858",
            "HAHA": "115940658764963", "WOW": "478547315650144", "SAD": "908563459236466", "ANGRY": "444813342392137"
        }
        starttime = str(datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f").timestamp()).replace('.', '')
        id_reac = reac.get(type)
        data = {
            'av': self.actor_id, 
            'fb_dtsg': self.fb_dtsg, 
            'jazoest': self.jazoest, 
            'lsd': self.lsd, 
            'fb_api_caller_class': 'RelayModern', 
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation', 
            'variables': '{"input":{"feedback_id":"'+encode_to_base64("feedback:"+str(id))+'","feedback_reaction_id":"'+id_reac+'","feedback_source":"TAHOE","is_tracking_encrypted":true,"session_id":"'+str(uuid.uuid4())+'","downstream_share_session_id":"'+str(uuid.uuid4())+'","downstream_share_session_start_time":"'+starttime+'","actor_id":"'+self.actor_id+'"},"useDefaultActor":false}', 
            'server_timestamps': 'true', 
            'doc_id': '7616998081714004',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return '{"data":{"feedback_react":{"feedback":{"id":' in response.text
        
    def share(self, id):
        data = {
            'av': self.actor_id,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ComposerStoryCreateMutation',
            'variables': '{"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\\"share_type\\":22,\\"share_params\\":['+id+']}"}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{"privacy":{"base_state":"EVERYONE"}},"is_tracking_encrypted":true,"actor_id":"'+self.actor_id+'"},"feedLocation":"NEWSFEED"}',
            'server_timestamps': 'true',
            'doc_id': '8167261726632010'
        }
        response = requests.post("https://www.facebook.com/api/graphql/", headers=self.headers, data=data, proxies=self.proxies)
        return '"errors"' not in response.text
        
    def like_page(self, id):
        data = {
            'av': self.actor_id,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometProfilePlusLikeMutation',
            'variables': '{"input":{"is_tracking_encrypted":false,"page_id":"'+str(id)+'","actor_id":"'+str(self.actor_id)+'"},"scale":1}',
            'server_timestamps': 'true',
            'doc_id': '6716077648448761',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return '"subscribe_status":"IS_SUBSCRIBED"' in response.text
    
    def group(self, id):
        data = {
            'av': self.actor_id,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'GroupCometJoinForumMutation',
            'variables': '{"groupID":"'+id+'","input":{"group_id":"'+id+'","actor_id":"self.actor_id"},"source":"GROUP_MALL"}',
            'server_timestamps': 'true',
            'doc_id': '5853134681430324',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return self.actor_id in response.text
    
    def follow(self, id):
        data = {
            'av': self.actor_id,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUserFollowMutation',
            'variables': '{"input":{"is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","actor_id":"'+str(self.actor_id)+'"},"scale":1}',
            'server_timestamps': 'true',
            'doc_id': '25581663504782089',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data, proxies=self.proxies)
        return '"subscribe_status":"IS_SUBSCRIBED"' in response.text
        
class NextCaptcha:
    def __init__(self, apikey):
        self.apikey = apikey
        self.create_task_url = "https://api.3xcaptcha.com/createTask"
        self.get_result_url = "https://api.3xcaptcha.com/getTaskResult"

    def recaptchav2(self, sitekey, siteurl):
        data = {
            "clientKey": self.apikey,
            "task": {
                "type": "RecaptchaV2TaskProxyless",
                "websiteURL": siteurl,
                "websiteKey": sitekey
            }
        }
        try:
            response = requests.post(self.create_task_url, json=data, timeout=10).json()
            if response.get("errorId", 0) != 0:
                return False, None
            return True, response.get("taskId")
        except:
            return False, None

    def get_result(self, task_id, max_retries=10, delay=0):
        data = {"clientKey": self.apikey, "taskId": task_id}
        for x in range(max_retries):
            try:
                response = requests.post(self.get_result_url, json=data, timeout=10).json()
                if response.get("errorId", 0) != 0:
                    return False, None
                if response.get("status") == "ready":
                    return True, response["solution"]["gRecaptchaResponse"]
                sleep(delay)
            except:
                return False, None
        return False, None

class TraoDoiSub_Api(object):
    def __init__(self, username, password, proxy=None) -> None:
        self.username = username
        self.password = password
        self.proxies = None
        self.session = requests.Session()
        self.headers = {'authority': 'traodoisub.com', 'accept': 'application/json, text/javascript, */*; q=0.01', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://traodoisub.com', 'referer': 'https://traodoisub.com/'}
        if proxy:
            try:
                proxy_parts = proxy.strip().split(':')
                if len(proxy_parts) == 4:
                    host, port, user, password = proxy_parts
                    self.proxies = {
                        'http': f'http://{user}:{password}@{host}:{port}',
                        'https': f'http://{user}:{password}@{host}:{port}'
                    }
            except:
                self.proxies = None
    
    def info(self):
        response = self.session.post('https://traodoisub.com/scr/login.php', headers=self.headers, data={'username': self.username, 'password': self.password}, proxies=self.proxies)
        if 'success' in response.text:
            self.cookie = response.headers['Set-cookie']
            headers = {'authority': 'traodoisub.com', 'cookie': self.cookie, 'user-agent': 'Mozilla/5.0'}
            response = self.session.get('https://traodoisub.com/view/setting/load.php', headers=headers).json()
            self.token = response['tokentds']
            self.xu = response['xu']
            self.name = response['user']
            return True, self.name, self.xu, self.token
        return False, None
        
    def facebook_configuration(self, id):
        try:
            response = self.session.post('https://traodoisub.com/scr/datnick.php', headers=self.headers, data={'iddat': id}, proxies=self.proxies).text
            return True if '1' in response else False
        except:
            return False

    def add_uid(self, id, g_recaptcha_response):
        headers = {'authority': 'traodoisub.com', 'cookie': self.cookie, 'user-agent': 'Mozilla/5.0'}
        response = self.session.post('https://traodoisub.com/scr/add_uid.php', headers=headers, data={'idfb': id, 'g-recaptcha-response': g_recaptcha_response}, proxies=self.proxies).text
        if 'success' in response: return True, None
        return False, response

    def get_g_recaptcha_response(self, apikey):
        try:
            response = requests.get('https://traodoisub.com/view/cauhinh/', headers=self.headers, proxies=self.proxies)
            sitekey = response.text.split('data-sitekey="')[1].split('"')[0]
            captcha_solver = NextCaptcha(apikey)
            success, task_id = captcha_solver.recaptchav2(sitekey, 'https://traodoisub.com/view/cauhinh/')
            if success:
                return captcha_solver.get_result(task_id)
        except:
            return False, 'Lỗi khi lấy reCAPTCHA'
        
    def get_nv_vip(self, fields, type):
        try: return self.session.get(f'https://traodoisub.com/api/?fields={fields}&access_token={self.token}&type={type}', proxies=self.proxies).json()
        except: return False
    
    def get_nv_thuong(self, fields):
        try: return self.session.get(f'https://traodoisub.com/api/?fields={fields}&access_token={self.token}', proxies=self.proxies).json()
        except: return False
    
    def get_xu_vip(self, type, id):
        try: return self.session.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', proxies=self.proxies).json()
        except: return False
    
    def get_xu_thuong(self, type, id):
        try: return self.session.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', proxies=self.proxies).json()
        except: return False
        
    def cache(self, type, id):
        try: return self.session.get(f'https://traodoisub.com/api/coin/?type={type}&id={id}&access_token={self.token}', proxies=self.proxies).json()
        except: return False

def Nhap_Cookie():
    demck = 0
    while True:
        demck += 1
        ck = input(f'{thanh} {luc}Nhập Cookie Facebook Thứ {vang}{demck}{trang}: ')
        if ck == '' and demck > 1: break
        fb = Facebook_Api(ck)
        info = fb.info()
        if 'success' in info:
            print(f'{thanh} {luc}Id Facebook: {vang}{info["id"]} {red}| {luc}Tên: {vang}{info["name"]}')
            listck.append(ck)
        else:
            print(f'{thanh} {red}Đăng Nhập Thất Bại!')
            demck -= 1
    return listck

def Nhap_Setting():
    apikey = input(f'{thanh} {luc}Nhập Api Key 3xcaptcha: {vang}')
    min = int(input(f'{thanh} {luc}Nhập Delay Min: {vang}'))
    max = int(input(f'{thanh} {luc}Nhập Delay Max: {vang}'))
    nvblock = int(input(f'{thanh} {luc}Nhiệm vụ chống block: {vang}'))
    delaybl = int(input(f'{thanh} {luc}Thời gian nghỉ ngơi: {vang}'))
    doinick = int(input(f'{thanh} {luc}Số nhiệm vụ đổi nick: {vang}'))
    nhiemvuloi = int(input(f'{thanh} {luc}Số nhiệm vụ lỗi để xóa Cookie: {vang}'))
    config = {"apikey": apikey, "min": min, "max": max, "nvblock": nvblock, "delaybl": delaybl, "doinick": doinick, "nhiemvuloi": nhiemvuloi}
    with open('settingch.json', 'w') as f: json.dump(config, f)
    return config

def Main():
    # Ép buộc hệ thống Windows CMD xóa sạch chữ hệ thống rác từ lịch sử trước khi in banner
    os.system('cls' if os.name == 'nt' else 'clear')
    
    ptool = 0
    dem = 0
    count = 0
    
    filename = "" 
    proxy_list = read_proxy_file(filename)
    proxy_index = 0
    current_proxy = 0
    myip = None
    if proxy_list:
        current_proxy = proxy_list[proxy_index]
        proxy_index = (proxy_index + 1) % len(proxy_list)
        username, password = current_proxy.split('@')[0].split(':')
        host, port = current_proxy.split('@')[1].split(':')
        data = {'listProxy': [{'username': username, 'password': password, 'host': host, 'port': int(port)}]}
        check = requests.post('https://api.proxymart.net/api/check-proxy', json=data).json()
        if check['data'][0]['isLive']: myip = check['data'][0]['ip']
        
    # Hệ thống chỉ gọi duy nhất 1 lần banner đổi màu tại đây sau khi chuẩn bị xong Proxy
    banner()  
    while True:
        if os.path.exists('acc_tds_log.txt'):
            with open('acc_tds_log.txt', 'r') as f: username, password = f.read().split('_')
            tds = TraoDoiSub_Api(username, password, current_proxy)
            profile = tds.info()
            try:
                print(f'{thanh} {luc}1. Chạy Tài Khoản {vang}{profile[1]} \n{thanh} {luc}2. Nhập Tài Khoản Mới')
                chon = input(f'{thanh} {luc}Nhập: ')
                if chon == '2': os.remove('acc_tds_log.txt')
                else: break
            except: os.remove('acc_tds_log.txt')
        if not os.path.exists('acc_tds_log.txt'):
            username, password = input(f'{thanh} {luc}Tài khoản TDS: '), input(f'{thanh} {luc}Mật khẩu TDS: ')
            with open('acc_tds_log.txt', 'w') as f: f.write(f'{username}_{password}')
    
    tds = TraoDoiSub_Api(username, password, current_proxy)
    profile = tds.info()
    user, xu = profile[1], profile[2]
    
    thanhngang(70)
    while True:
        if os.path.exists('Cookie_FB.txt'):
            print(f'{thanh} {luc}1. Dùng Cookie Đã Lưu \n{thanh} {luc}2. Nhập Cookie Mới')
            if input(f'{thanh} {luc}Nhập: ') == '1':
                with open('Cookie_FB.txt', 'r') as f: listck = json.loads(f.read())
                break
            else: os.remove('Cookie_FB.txt')
        if not os.path.exists('Cookie_FB.txt'):
            listck = Nhap_Cookie()
            with open('Cookie_FB.txt', 'w') as f: json.dump(listck, f)
            break
    os.system('cls' if os.name == 'nt' else 'clear')            
    banner()
    print(f'{thanh} {luc}Tài khoản: {vang}{user} | Xu: {vang}{str(format(int(xu),","))} | FB Accs: {vang}{len(listck)} | Proxy IP: {vang}{myip}')
    thanhngang(70)
    print(f'1: CX_Vip | 2: CxCmt_Vip | 3: Share_Vip | 4: Follow_Vip | 5: Page_Vip | 6: Group | 7: Share_Thường | 8: Page_Thường | 9: Like_Thường | 0: CX_Thường')
    nhap = input(f'{thanh} {luc}Chọn nhiệm vụ (Ví dụ: 123): ')
    listnv.append(nhap.replace(' ', ''))
    
    thanhngang(70)
    if os.path.exists('settingch.json'):
        with open('settingch.json', 'r') as f: config = json.load(f)
        if input(f'{thanh} {luc}Dùng cấu hình cũ không? (y/n): ') == 'y':
            apikey, min, max, nvblock, delaybl, doinick, nhiemvuloi = config['apikey'], config['min'], config['max'], config['nvblock'], config['delaybl'], config['doinick'], config['nhiemvuloi']
        else:
            os.remove('settingch.json')
            config = Nhap_Setting()
            apikey, min, max, nvblock, delaybl, doinick, nhiemvuloi = config['apikey'], config['min'], config['max'], config['nvblock'], config['delaybl'], config['doinick'], config['nhiemvuloi']
    else:
        config = Nhap_Setting()
        apikey, min, max, nvblock, delaybl, doinick, nhiemvuloi = config['apikey'], config['min'], config['max'], config['nvblock'], config['delaybl'], config['doinick'], config['nhiemvuloi']
        
    chonan = input(f'{thanh} {luc}Ẩn ID Facebook? (y/n): ')
    thanhngang(70)
    
    while True:
        if len(listck) == 0:
            listck = Nhap_Cookie()
            with open('Cookie_FB.txt', 'w') as f: json.dump(listck, f)
        for ck in listck:
            nhiemvu = listnv[0]
            loireaction, loicxcmt, loishare, loifollow, loipage, loigr, loilike, loiliket, loisharet = 0, 0, 0, 0, 0, 0, 0, 0, 0
            fb = Facebook_Api(ck, current_proxy)
            info = fb.info()
            if 'success' in info:
                name, uid = info['name'], info['id']
                uid2 = uid[:3]+'#'*(len(uid)-6)+uid[-3:] if chonan == 'y' else uid
            else:
                listck.remove(ck)
                continue
                
            if tds.facebook_configuration(uid):
                print(f'{luc}Id FB: {vang}{uid2} | Tên: {vang}{name}')
            else:
                if apikey:
                    get_g_recaptcha_response = tds.get_g_recaptcha_response(apikey)
                    if get_g_recaptcha_response[0] and tds.add_uid(uid, get_g_recaptcha_response[1])[0] and tds.facebook_configuration(uid):
                        print(f'{luc}Id FB: {vang}{uid2} | Tên: {vang}{name}')
                        
            ptool = 0
            while True:
                if ptool == 1 or nhiemvu == '': break
                
                if '1' in nhiemvu:
                    listcx = tds.get_nv_vip('facebook_reaction', 'ALL')
                    if listcx and 'data' in listcx:
                        for x in listcx['data']:
                            id = x['id'].split('_')[1] if '_' in x['id'] else x['id']
                            id2 = id[:3]+'#'*(len(id)-6)+id[-3:]
                            if fb.reaction(id, x['type']):
                                nhan = tds.get_xu_vip('facebook_reaction', x['code'])
                                if 'success' in nhan:
                                    dem += 1
                                    print(f'{red}[{dem}][{datetime.now().strftime("%H:%M:%S")}][{x["type"]}][{id2}][{nhan["data"]["msg"]}][{myip}]')
                                    if dem % doinick == 0: ptool = 1; break
                                    if dem % nvblock == 0: Delay(delaybl)
                                    else: Delay(randint(min, max))
                            else:
                                loireaction += 1
                        if loireaction >= nhiemvuloi: nhiemvu = nhiemvu.replace('1','')

                ptool = 1 

if __name__ == "__main__":
    Main()