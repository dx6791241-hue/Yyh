import json
import os
import sys
import time
import requests
import re
import uuid
import random
import socket
import subprocess
import io
import base64
from datetime import datetime, timedelta
from time import sleep, strftime
from bs4 import BeautifulSoup
from colorama import Fore, init
from pystyle import Write, Colors, Colorate
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Cấu hình encoding chống lỗi hiển thị ký tự đặc biệt trên CMD Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# =====================================================================
# 🟩 KHU VỰC BANNER & GIAO DIỆN (UI) - GIỮ NGUYÊN HOẠT ĐỘNG
# =====================================================================
def banner():
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
#  MÀU SẮC & HIỆU ỨNG GRADIENT (HÀM BỔ TRỢ)
# =====================================================================
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
tim = "\033[1;35m"
xanh = "\033[1;36m"
dep = "\033[38;2;160;231;229m"
v = "\033[38;2;220;200;255m"
thanh = f'\033[1;35m {trang}=> '
unicode_invisible = ("ㅤ")

def gradient_3(text):
    def rgb_to_ansi(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    start, end = (0, 255, 0), (0, 128, 255)
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
    start_color, mid_color, end_color = (255, 87, 34), (255, 20, 147), (255, 255, 0)
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

def gradient(text, start_color=(255, 0, 255), end_color=(0, 255, 255)):
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (length - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (length - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (length - 1))
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + "\033[0m"

def thanhngang(so):
    print(trang + '═' * so)

def Delay(value):
    while not(value <= 1):
        value -= 0.123
        print(f'''{v}[{xanh}OBIIYEUEM{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [{vang}BANANAHUB   {v}]''', '           ', end = '\r')
        sleep(0.005)
        print(f'''{v}[{xanh}OBIIYEUEM{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [ {vang}BANANAHUB   {v}]''', '           ', end = '\r')
        sleep(0.005)
        print(f'''{v}[{xanh}OBIIYEUEM{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [  {vang}BANANAHUB {v}]''', '            ', end = '\r')
        sleep(0.005)
        print(f'''{v}[{xanh}OBIIYEUEM{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [   {vang}BANANAHUB {v}]''', '           ', end = '\r')
        sleep(0.005)
        print(f'''{v}[{xanh}OBIIYEUEM{v}] [{xanh}DELAY{v}] [{xanh}{str(value)[0:6]}{v}] [    {vang}BANANAHUB {v}]''', '           ', end = '\r')
        sleep(0.005)

def decode_base64(encoded_str):
    return base64.b64decode(encoded_str).decode('utf-8')

def encode_to_base64(_data):
    return base64.b64encode(_data.encode('utf-8')).decode('utf-8')


# =====================================================================
#  LỚP ĐIỀU HƯỚNG & THAO TÁC FACEBOOK (API GRAPHQL) - ĐÃ FIX INDENT
# =====================================================================
class Facebook:
    def __init__(self, cookie: str):
        try:
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.session = requests.Session()
            self.id = self.cookie.split('c_user=')[1].split(';')[0]
            self.headers = {
                'authority': 'www.facebook.com', 
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 
                'accept-language': 'vi', 
                'sec-ch-ua-mobile': '?0', 
                'sec-ch-ua-platform': '"Windows"', 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 
                'Cookie': self.cookie
            }
            url = self.session.get(f'https://www.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            
            if '828281030927956' in response.text: return '956'
            if '1501092823525282' in response.text: return '282'
            if '601051028565049' in response.text: return 'spam'
            
            name_match = re.search(r'"NAME":"([^"]+)"', response.text)
            if name_match:
                name = name_match.group(1).encode('utf-8').decode('unicode_escape', errors='ignore')
            else:
                name = 'Clone Không Tên (Bypass)'
                
            if self.id:
                return {'success': 200, 'id': self.id, 'name': name}
            return 'cookieout'
        except Exception as e:
            return 'cookieout'
        
    def likepage(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometProfilePlusLikeMutation','variables': '{"input":{"is_tracking_encrypted":false,"page_id":"'+str(id)+'","source":null,"tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"1"},"scale":1}','server_timestamps': 'true','doc_id': '6716077648448761',}
            return '"subscribe_status":"IS_SUBSCRIBED"' in self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers).text
        except: return False

    def follow(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUserFollowMutation','variables': '{"input":{"attribution_id_v2":"","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'+str(id)+'","tracking":null,"actor_id":"'+str(self.id)+'","client_mutation_id":"5"},"scale":1}','server_timestamps': 'true','doc_id': '25581663504782089',}
            return '"subscribe_status":"IS_SUBSCRIBED"' in self.session.post('https://www.facebook.com/api/graphql/',data=data,headers=self.headers).text
        except: return False

    def reaction(self, id: str, type: str):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': fr'{{"input":{{"feedback_id":"{encode_to_base64("feedback:"+str(id))}","feedback_reaction_id":"{reac.get(type)}","feedback_source":"NEWS_FEED","is_tracking_encrypted":true,"session_id":"{uuid.uuid4()}","actor_id":"{self.id}","client_mutation_id":"3"}},"useDefaultActor":false}}','server_timestamps': 'true','doc_id': '7047198228715224',}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: pass

    def reactioncmt(self, id: str, type: str):
        try:
            reac = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
            starttime = str(datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f").timestamp()).replace('.', '')
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation','variables': '{"input":{"feedback_id":"'+encode_to_base64("feedback:"+str(id))+'","feedback_reaction_id":"'+reac.get(type)+'","feedback_source":"TAHOE","is_tracking_encrypted":true,"session_id":"'+str(uuid.uuid4())+'","downstream_share_session_id":"'+str(uuid.uuid4())+'","downstream_share_session_start_time":"'+starttime+'","actor_id":"'+self.id+'","client_mutation_id":"1"},"useDefaultActor":false}', 'server_timestamps': 'true','doc_id': '7616998081714004',}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: pass
    
    def share(self, id: str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'ComposerStoryCreateMutation','variables': '{"input":{"composer_entry_point":"share_modal","composer_source_surface":"feed_story","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\\"share_type\\":22,\\"share_params\\":['+id+']}"}}],"reshare_original_post":"RESHARE_ORIGINAL_POST","audience":{"privacy":{"base_state":"EVERYONE"}},"actor_id":"'+self.id+'"},"feedLocation":"NEWSFEED","scale":1}','server_timestamps': 'true','doc_id': '8167261726632010'}
            self.session.post("https://www.facebook.com/api/graphql/",headers=self.headers, data=data)
        except: pass

    def group(self, id: str):
        try:
            data = {'av':self.id,'fb_dtsg':self.fb_dtsg,'jazoest':self.jazoest,'fb_api_caller_class':'RelayModern','fb_api_req_friendly_name':'GroupCometJoinForumMutation','variables':'{"groupID":"'+id+'","input":{"group_id":"'+id+'","actor_id":"'+self.id+'"},"source":"GROUP_MALL"}','server_timestamps':'true','doc_id':'5853134681430324'}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: pass

    def comment(self, id, msg:str):
        try:
            data = {'av': self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'fb_api_caller_class': 'RelayModern','fb_api_req_friendly_name': 'useCometUFICreateCommentMutation','variables': fr'{{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"input":{{"actor_id":"{self.id}","feedback_id":"{encode_to_base64(f"feedback:{id}")}","message":{{"text":"{msg}"}},"idempotence_token":"client:{uuid.uuid4()}","session_id":"{uuid.uuid4()}"}}}}','server_timestamps': 'true','doc_id': '7994085080671282'}
            self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
        except: pass
    
    def page_review(self, id, msg:str):
        try:
            data = {'av':self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'variables': '{"input":{"composer_entry_point":"inline_composer","source":"WWW","audience":{"privacy":{"base_state":"EVERYONE"}},"message":{"text":"' +msg+ '"},"page_recommendation":{"page_id":"'+id+'","rec_type":"POSITIVE"},"actor_id":"'+self.id+'"},"feedLocation":"PAGE_SURFACE_RECOMMENDATIONS"}','doc_id': '5737011653023776'}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: pass
    
    def sharend(self, id, msg:str):
        try:
            data = {'av':self.id,'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'variables': '{"input":{"composer_entry_point":"share_modal","composer_type":"share","idempotence_token":"'+str(uuid.uuid4())+'_FEED","source":"WWW","attachments":[{"link":{"share_scrape_data":"{\\"share_type\\":22,\\"share_params\\":['+id+']}"}}],"audience":{"privacy":{"base_state":"EVERYONE"}},"message":{"text":"'+msg+'"},"actor_id":"'+self.id+'"},"feedLocation":"NEWSFEED"}','doc_id': '29449903277934341'}
            self.session.post('https://www.facebook.com/api/graphql/',headers=self.headers, data=data)
        except: pass

    def checkDissmiss(self):
        try:
            response = self.session.get('https://www.facebook.com/', headers=self.headers)
            if '601051028565049' in response.text: return 'Dissmiss'
            if '1501092823525282' in response.text: return 'Checkpoint282'
            if '828281030927956' in response.text: return 'Checkpoint956'
            if 'title="Log in to Facebook">' in response.text: return 'CookieOut'
            return 'Biblock'
        except: return 'CookieOut'
    
    def clickDissMiss(self):
        try:
            data = {"av": self.id,"fb_dtsg": self.fb_dtsg,"jazoest": self.jazoest,"fb_api_caller_class": "RelayModern","fb_api_req_friendly_name": "FBScrapingWarningMutation","variables": "{}","server_timestamps": "true","doc_id": "6339492849481770"}
            self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data)
        except: pass


# =====================================================================
#  LỚP KẾT NỐI API TƯƠNG TÁC CHÉO
# =====================================================================
class TuongTacCheo(object):
    def __init__ (self, token):
        try:
            self.ss = requests.Session()
            session = self.ss.post('https://tuongtaccheo.com/logintoken.php',data={'access_token': token})
            self.cookie = session.headers['Set-cookie']
            self.session = session.json()
            self.headers = {
                'Host': 'tuongtaccheo.com',
                'accept': '*/*',
                'origin': 'https://tuongtaccheo.com',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                "cookie": self.cookie
            }
        except: pass

    def info(self):
        if self.session.get('status') == 'success':
            return {'status': "success", 'user': self.session['data']['user'], 'xu': self.session['data']['sodu']}
        return {'error': 200}
        
    def cauhinh(self, id):
        response = self.ss.post('https://tuongtaccheo.com/cauhinh/datnick.php',headers=self.headers, data={'iddat[]': id, 'loai': 'fb'}).text
        if response == '1': return {'status': "success", 'id': id}
        return {'error': 200}
        
    def getjob(self, nv):
        return self.ss.get(f'https://tuongtaccheo.com/kiemtien/{nv}/getpost.php', headers=self.headers)
    
    def nhanxu(self, id, nv):
        try:
            xu_truoc = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
            response = self.ss.post(f'https://tuongtaccheo.com/kiemtien/{nv}/nhantien.php', headers=self.headers, data={'id': id}).json()
            xu_sau = self.ss.get('https://tuongtaccheo.com/home.php', headers=self.headers).text.split('"soduchinh">')[1].split('<')[0]
            if 'mess' in response and int(xu_sau) > int(xu_truoc):
                return {'status': "success", 'msg': '+'+response['mess'].split()[-2]+' Xu', 'xu': xu_sau} 
            return {'error': response}
        except: return {'error': 'Failed'}


# =====================================================================
#  HÀM QUẢN LÝ COOKIE & ĐĂNG NHẬP
# =====================================================================
def addcookie(listCookie):
    i = len(listCookie)
    while True:
        i += 1
        cookie = input(f'{thanh}{luc}Nhập Cookie Facebook Số{vang} {i}{trang}: {vang}')
        if cookie == '' and i != 1: break 
        fb = Facebook(cookie)
        info = fb.info()
        if isinstance(info, dict) and 'success' in info:
            print(f'{thanh}{luc}Username: {vang}{info["name"]}')
            print(gradient("-"*50))
            listCookie.append(cookie)
        else:
            print(f'{do}Cookie Facebook Die ! Vui Lòng Nhập Lại !!!')
            i -= 1

def login_ttc():
    if not os.path.exists('tokenttcfb.json'):
        while True:
            token = input(f'{thanh}\033[38;2;0;255;0m Nhập Access_Token TTC{trang}:{vang} ')
            print('\033[1;36mĐang Xử Lý....', '     ', end='\r')
            ttc = TuongTacCheo(token)
            checktoken = ttc.info()
            if checktoken.get('status') == 'success':
                print(f"{luc}Đăng Nhập Thành Công")
                with open('tokenttcfb.json', 'w') as f:
                    json.dump([token + '|' + checktoken['user']], f)
                return ttc, checktoken
            print(f'{do}Đăng Nhập Thất Bại')
    else:
        token_json = json.loads(open('tokenttcfb.json', 'r').read())
        stt_token = 0
        for tokens in token_json:
            if len(tokens) > 5:
                stt_token += 1
                print(f'{thanh}{luc}Nhập {do}[{vang}{stt_token}{do}] {luc}Để Chạy Tài Khoản: {vang}{tokens.split("|")[1]}')
        print(gradient("-"*50))
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Chọn Acc Tương Tác Chéo Để Chạy Tool')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Access_Token Tương Tác Chéo Mới')
        print(gradient("-"*50))
        while True:
            chon = input(f'{thanh}{luc}Nhập: {vang}')
            print(gradient("-"*50))
            if chon == '1':
                while True:
                    try:
                        tokenttcfb = int(input(f'{thanh}{luc}Nhập Số Acc: {vang}'))
                        print(gradient("-"*50))
                        ttc = TuongTacCheo(token_json[tokenttcfb - 1].split("|")[0])
                        checktoken = ttc.info()
                        if checktoken.get('status') == 'success':
                            print(f"{luc}Đăng Nhập Thành Công")
                            return ttc, checktoken
                        print(f'{do}Đăng Nhập Thất Bại')
                    except: print(f'{do}Số Acc Không Tồn Tại')
            elif chon == '2':
                while True:
                    token = input(f'{thanh}{luc}Nhập Access_Token TTC{trang}: {vang}')
                    print('\033[1;32mĐang Xử Lý....', '     ', end='\r')
                    ttc = TuongTacCheo(token)
                    checktoken = ttc.info()
                    if checktoken.get('status') == 'success':
                        print(f"{luc}Đăng Nhập Thành Công")
                        token_json.append(token + '|' + checktoken['user'])
                        with open('tokenttcfb.json', 'w') as f:
                            json.dump(token_json, f)
                        return ttc, checktoken
                    print(f'{do}Đăng Nhập Thất Bại')
            else: print(f'{do}Vui Long Nhập Chính Xác ')

def setup_cookies():
    listCookie = []
    if not os.path.exists('cookiefb-ttc.json'):
        addcookie(listCookie)
        with open('cookiefb-ttc.json', 'w') as f:
            json.dump(listCookie, f)
    else:
        print(f'{thanh}{luc}Nhập {do}[{vang}1{do}] {luc}Sử Dụng Cookie Facebook Đã Lưu')
        print(f'{thanh}{luc}Nhập {do}[{vang}2{do}] {luc}Nhập Cookie Facebook Mới')
        print(gradient("-"*50))
        chon = input(f'{thanh}{luc}Nhập{trang}: {vang}')
        print(gradient("-"*50))
        while True:
            if chon == '1':
                print(f'{luc}Đang Lấy Dữ Liệu Đã Lưu ', '          ', end='\r')
                sleep(1)
                listCookie = json.loads(open('cookiefb-ttc.json', 'r').read())
                break
            elif chon == '2':
                addcookie(listCookie)
                with open('cookiefb-ttc.json', 'w') as f:
                    json.dump(listCookie, f)
                break
            else: print(f'{do}Vui Lòng Nhập Đúng !!!')
    return listCookie


# =====================================================================
#  HÀM CẤU HÌNH THỜI GIAN & HỆ THỐNG MENU NHIỆM VỤ
# =====================================================================
def menu_nhiemvu(users, checktoken, listCookie):
    os.system("cls" if os.name == "nt" else "clear")            
    banner()
    print(f'{thanh}{luc}Facebook Name{trang}: {vang}{users}')
    print(f'{thanh}{luc}Total Coin{trang}: {vang}{str(format(int(checktoken["xu"]), ","))}')
    print(f'{thanh}{luc}Total Cookie Facebook{trang}: {vang}{len(listCookie)}')
    print(gradient("-"*50))
    print(f'{thanh}{dep}Nhập [{vang}1{do}]{dep} Đang Chạy NV Like Vip          Nhập [{vang}2{do}]{dep} Đang Chạy NV Like Thường')
    print(f'{thanh}{dep}Nhập [{vang}3{do}]{dep} Đang Chạy NV Cảm Xúc Vip       Nhập [{vang}4{do}]{dep} Đang Chạy NV Cảm Xúc Thường')
    print(f'{thanh}{dep}Nhập [{vang}5{do}]{dep} Đang Chạy NV Cảm Xúc Comment   Nhập [{vang}6{do}]{dep} Đang Chạy NV Comment')
    print(f'{thanh}{dep}Nhập [{vang}7{do}]{dep} Đang Chạy NV Share             Nhập [{vang}8{do}]{dep} Đang Chạy NV Like Page')
    print(f'{thanh}{dep}Nhập [{vang}9{do}]{dep} Đang Chạy NV Follow            Nhập [{vang}0{do}]{dep} Đang Chạy NV Group')
    print(f'{thanh}{dep}Nhập [{vang}q{do}]{dep} Đang Chạy NV Review            Nhập [{vang}s{do}]{dep} Đang Chạy NV Share Nội Dung')
    print(f'{thanh}{dep}Có Thể Chọn Nhiều Nhiệm Vụ {do}({vang}VD: 123...{do})')
    print(gradient("-"*50))
    
    nhiemvu = str(input(f'{thanh}\033[38;2;220;200;255mNhập Số Để Chọn Nhiệm Vụ{trang}: {vang}'))
    list_nv = [x for x in nhiemvu if x in ['1','2','3','4','5','6','7','8','9','0', 'q', 's']]
    
    while True:
        try:
            delay = int(input(f'{thanh}{v}Nhập Delay Job{trang}: {vang}'))
            break
        except: print(f'{do}Vui Lòng Nhập Số')
    while True:
        try:
            JobbBlock = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chống Block{trang}: {vang}'))
            if JobbBlock > 1: break
            print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        except: print(f'{do}Vui Lòng Nhập Số')
    while True:
        try:
            DelayBlock = int(input(f'{thanh}{v}Sau {vang}{JobbBlock} {v}Nhiệm Vụ Nghỉ Bao Nhiêu Giây{trang}: {vang}'))
            break
        except: print(f'{do}Vui Lòng Nhập Số')
    while True:
        try:
            JobBreak = int(input(f'{thanh}{v}Sau Bao Nhiêu Nhiệm Vụ Chuyển Acc{trang}: {vang}'))
            if JobBreak > 1: break
            print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        except: print(f'{do}Vui Lòng Nhập Số')
        
    runidfb = input(f'{thanh}{v}Bạn Có Muốn Ẩn Id Facebook Không? {do}({vang}y/n{do}){v}: {vang}')
    print(gradient("-"*50))
    return list_nv, delay, JobbBlock, DelayBlock, JobBreak, runidfb


# =====================================================================
#  HÀM LOGIC THỰC THI NHIỆM VỤ (MAIN LOOP EXECUTION)
# =====================================================================
def run_bot(ttc, checktoken, listCookie, list_nv, delay, JobbBlock, DelayBlock, JobBreak, runidfb):
    stt = 0
    totalxu = 0
    while True:
        if len(listCookie) == 0:
            print(f'{do}Đã Xóa Tất Cả Cookie, Vui Lòng Nhập Lại !!!')
            addcookie(listCookie)
            with open('cookiefb-ttc.json', 'w') as f: json.dump(listCookie, f)
            
        for cookie in listCookie:
            JobError, JobSuccess, JobFail = 0, 0, 0
            fb = Facebook(cookie)
            info = fb.info()
            
            if isinstance(info, dict) and 'success' in info:
                namefb = info['name']
                idfb = str(info['id'])
                idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if runidfb.upper() =='Y' else idfb
            else:
                print(f'{do}Cookie Facebook Die ! Đã Xóa Ra Khỏi List !!!')
                listCookie.remove(cookie)
                break
                
            cauhinh = ttc.cauhinh(idfb)
            if cauhinh.get('status') == 'success':
                print(f'{luc}Id Facebook{trang}: {vang}{idrun}{do} | {luc}Facebook Name{trang}: {vang}{namefb}')
            else:
                print(f'{luc}Chưa Cấu Hình Id Facebook{trang}: {vang}{idfb}{do} | {luc}Tên Tài Khoản{trang}: {vang}{namefb}')
                listCookie.remove(cookie)
                break
                
            list_nv_default = list_nv.copy()
            while True:
                random_nv = random.choice(list_nv)
                mapping_nv = {
                    '1': ('likepostvipcheo', 'LIKE'), '2': ('likepostvipre', 'LIKE'),
                    '3': ('camxucvipcheo', 'CX_VIP'), '4': ('camxuccheo', 'CX'),
                    '5': ('camxuccheobinhluan', 'CX_CMT'), '6': ('cmtcheo', 'COMMENT'),
                    '7': ('sharecheo', 'SHARE'), '8': ('likepagecheo', 'LIKEPAGE'),
                    '9': ('subcheo', 'FOLLOW'), '0': ('thamgianhomcheo', 'GROUP'),
                    'q': ('danhgiapage', 'REVIEW'), 's': ('sharecheokemnoidung', 'SHAREND')
                }
                fields, type_name = mapping_nv[random_nv]
                chuyen = False
                
                try:
                    getjob = ttc.getjob(fields)
                    if "idpost" in getjob.text or "idfb" in getjob.text or "UID" in getjob.text:
                        print(luc+f" Đã Tìm Thấy {len(getjob.json())} Nhiệm Vụ {fields.title()}       ", end="\r")
                        for x in getjob.json():
                            nextDelay = False
                            
                            if random_nv in ["1", "2"]:
                                trg_id = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']
                                fb.reaction(trg_id, "LIKE"); id_ = trg_id; id = x['idpost']
                            elif random_nv == "3":
                                trg_id = x['idfb'].split('_')[1] if '_' in x['idfb'] else x['idfb']
                                fb.reaction(trg_id, x['loaicx']); id_ = trg_id; id = x['idpost']
                            elif random_nv in ["4", "5"]:
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                if random_nv == "4": fb.reaction(trg_id, x['loaicx'])
                                else: fb.reactioncmt(trg_id, x['loaicx'])
                                id_ = trg_id; id = x['idpost']
                            elif random_nv == "6":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.comment(trg_id, json.loads(x["nd"])[0]); id_ = trg_id; id = x['idpost']
                            elif random_nv == "7":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.share(trg_id); id_ = trg_id; id = x['idpost']
                            elif random_nv == "8":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.likepage(trg_id); id_ = trg_id; id = x['idpost']
                            elif random_nv == "9":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.follow(trg_id); id_ = trg_id; id = x['idpost']
                            elif random_nv == "0":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.group(trg_id); id_ = trg_id; id = x['idpost']
                            elif random_nv == 'q':
                                trg_id = x['UID'].split('_')[1] if '_' in x['UID'] else x['UID']
                                fb.page_review(trg_id, json.loads(x["nd"])[0]); id_ = trg_id; id = x['UID']
                            elif random_nv == "s":
                                trg_id = x['idpost'].split('_')[1] if '_' in x['idpost'] else x['idpost']
                                fb.sharend(trg_id, json.loads(x["nd"])[0]); id_ = trg_id; id = x['idpost']

                            nhanxu = ttc.nhanxu(id, fields)
                            if nhanxu.get('status') == 'success':
                                nextDelay, msg, xu, JobFail, timejob = True, nhanxu['msg'], nhanxu['xu'], 0, datetime.now().strftime('%H:%M:%S')
                                totalxu += int(msg.replace(' Xu', ''))
                                stt += 1
                                JobSuccess += 1
                                print(f'{do}[ \033[1;36m{stt}{do} ] {do}[ {vang}HectorVN{do} ][ {xanh}{timejob}{do} ][ {vang}{type_name}{do} ][ {trang}{id_}{do} ][ {vang}{msg}{do} ][ {luc}{str(format(int(xu),","))} {do}]')
                                if stt % 10 == 0:
                                    print(f'{trang}[{luc}Total Cookie Facebook: {vang}{len(listCookie)}{trang}] [{luc}Total Coin: {vang}{str(format(int(totalxu),","))}{trang}] [{luc}Tổng Xu: {vang}{str(format(int(xu),","))}{trang}]')
                            else:
                                JobFail += 1
                                print(f'{trang}[{do}{JobFail}{trang}] {trang}[{do}ERROR{trang}] {trang}{id_}', '            ', end="\r")
                            
                            if JobFail >= 20:
                                check = fb.info()
                                if 'spam' in check:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Spam')
                                    fb.clickDissMiss()
                                elif '282' in check:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Checkpoint282')
                                    listCookie.remove(cookie); chuyen = True; break
                                elif '956' in check:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Checkpoint956')
                                    listCookie.remove(cookie); chuyen = True; break
                                elif 'cookieout' in check:
                                    print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Out Cookie, Đã Xoá Khỏi List')
                                    listCookie.remove(cookie); chuyen = True; break
                                else:
                                    print(do+f'Tài Khoản {vang}{namefb} {do}Đã Bị Block {fields.upper()}')
                                    JobFail = 0
                                    if random_nv in list_nv: list_nv.remove(random_nv)
                                    if list_nv: random_nv = random.choice(list_nv)
                                    else:
                                        print(f'{do}Tài Khoản {vang}{namefb} {do}Đã Bị Block Tất Cả Tương Tác')
                                        listCookie.remove(cookie); chuyen = True; list_nv = list_nv_default.copy()
                                        break

                            if JobSuccess != 0 and JobSuccess % int(JobBreak) == 0:
                                chuyen = True; break

                            if nextDelay:
                                if stt % int(JobbBlock) == 0: Delay(DelayBlock)
                                else: Delay(delay)

                        if chuyen: break
                    else:
                        if 'error' in getjob.text and getjob.json().get('countdown'):
                            print(f'{do}Tiến Hành Get Job {fields.upper()}, COUNTDOWN: {str(round(getjob.json()["countdown"], 3))}', end="\r")
                            sleep(1); Delay(getjob.json()['countdown'])
                except: pass


# =====================================================================
#  HÀM KHỞI CHẠY CHÍNH (MAIN FUNCTION)
# =====================================================================
def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    
    # 1. Đăng nhập hệ thống TTC
    ttc, checktoken = login_ttc()
    
    # 2. Đồng bộ Cookie tài khoản Facebook công việc
    listCookie = setup_cookies()
    
    # 3. Hiện Menu cấu hình nhiệm vụ
    list_nv, delay, JobbBlock, DelayBlock, JobBreak, runidfb = menu_nhiemvu(checktoken['user'], checktoken, listCookie)
    
    # 4. Bắt đầu luồng chạy nhiệm vụ chính
    run_bot(ttc, checktoken, listCookie, list_nv, delay, JobbBlock, DelayBlock, JobBreak, runidfb)

if __name__ == "__main__":
    main()
