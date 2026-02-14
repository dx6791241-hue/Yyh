# Hyperion deobf by KhanhNguyen9872
# FB: https://fb.me/khanh10a1
# File name: [deobf_layer_1_dump_2_tym.py] (py - 3.11)

from builtins import all,exec,format,id,print,int,range,set,str,open,quit
exec('')
import os
try:
	import requests,colorama,prettytable
except:
	os.system('pip install requests')
	os.system('pip install colorama')
	os.system('pip install prettytable')
import threading,requests,ctypes,random,json,time,base64,sys,re
from prettytable import PrettyTable
import random
from time import strftime
from colorama import init,Fore
from urllib.parse import urlparse,unquote,quote
from string import ascii_letters,digits
class Zefoy:
	def __init__(self):
		self.base_url='https://zefoy.com/'
		self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
		self.session=requests.Session()
		self.captcha_1=None
		self.captcha_={}
		self.service='Hearts'
		self.video_key=None
		self.services={}
		self.services_ids={}
		self.services_status={}
		self.url='None'
		self.text='Nguyên'
		url1=Write.Input(('</> Nhập link video: '),Colors.red_to_white,interval=0.001)
		self.url=url1
	def get_captcha(self):
		if os.path.exists('session'):self.session.cookies.set('PHPSESSID',open('session',encoding='utf-8').read(),domain='zefoy.com')
		request=self.session.get(self.base_url,headers=self.headers)
		if 'Enter Video URL' in request.text:self.video_key=request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]; return True
		try:
			for x in re.findall('<input type="hidden" name="(.*)" value="(.*)">',request.text):self.captcha_[x[0]]=x[1]
			self.captcha_1=request.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
			captcha_url=request.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0]
			request=self.session.get(f"{self.base_url}{captcha_url}",headers=self.headers)
			open('captcha.png','wb').write(request.content)
			Write.Print(('</> Đang giải capcha..\n'),Colors.red_to_white,interval=0.001)
			return False
		except Exception as e:
			Write.Print((f"</> Không thể giải captcha: {e}\n"),Colors.red_to_white,interval=0.001)
			time.sleep(2)
			self.get_captcha()
	def send_captcha(self,new_session=False):
		if new_session:self.session=requests.Session(); os.remove('session'); time.sleep(2)
		if self.get_captcha():Write.Print(('</> Đang kêt nối đến session\n'),Colors.red_to_white,interval=0.001);return(True,'The session already exists')
		captcha_solve=self.solve_captcha('captcha.png')[1]
		self.captcha_[self.captcha_1]=captcha_solve
		request=self.session.post(self.base_url,headers=self.headers,data=self.captcha_)
		if 'Enter Video URL' in request.text:
			Write.Print(('</> Session đã được tạo\n'),Colors.red_to_white,interval=0.001)
			open('session','w',encoding='utf-8').write(self.session.cookies.get('PHPSESSID'))
			Write.Print((f"</> Giải capcha thành công: {captcha_solve}\n"),Colors.red_to_white,interval=0.001)
			self.video_key=request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
			return(True,captcha_solve)
		else:return(False,captcha_solve)
	def solve_captcha(self,path_to_file=None,b64=None,delete_tag=['\n','\r']):
		if path_to_file:task=path_to_file
		else:open('temp.png','wb').write(base64.b64decode(b64)); task='temp.png'
		request=self.session.post('https://api.ocr.space/parse/image?K87899142388957',headers={'apikey':'K87899142388957'},files={'task':open(task,'rb')}).json()
		solved_text=request['ParsedResults'][0]['ParsedText']
		for x in delete_tag:solved_text=solved_text.replace(x,'')
		return(True,solved_text)
	def get_status_services(self):
		request=self.session.get(self.base_url,headers=self.headers).text
		for x in re.findall('<h5 class="card-title">.+</h5>\n.+\n.+',request):self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()]=x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
		for x in re.findall('<h5 class="card-title mb-3">.+</h5>\n<form action=".+">',request):self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()]=x.split('<form action="')[1].split('">')[0].strip()
		for x in re.findall('<h5 class="card-title">.+</h5>\n.+<button .+',request):self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()]=False if 'disabled class' in x else True
		return(self.services,self.services_status)
	def find_video(self):
		if self.service is None:return(False,"You didn't choose the service")
		while True:
			if self.service not in self.services_ids:self.get_status_services(); time.sleep(1)
			request=self.session.post(f'{self.base_url}{self.services_ids[self.service]}',headers={'content-type':'multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ','user-agent':self.headers['user-agent'],'origin':'https://zefoy.com'},data=f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.video_key}"\r\n\r\n{self.url}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n')
			try:self.video_info=base64.b64decode(unquote(request.text.encode()[::-1])).decode()
			except:time.sleep(3); continue
			if 'Session expired. Please re-login' in self.video_info:Write.Print(('</> Phiên hết hạn. Đang đăng nhập lại...\n'),Colors.red_to_white,interval=0.001);self.send_captcha(); return
			elif 'service is currently not working' in self.video_info:return(True,'[Nguyên]</> Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.')
			elif 'onsubmit="showHideElements' in self.video_info:
				self.video_info=[self.video_info.split('" name="')[1].split('"')[0],self.video_info.split('value="')[1].split('"')[0]]
				return(True,request.text)
			elif 'Checking Timer...' in self.video_info:
				try:
					t=int(re.findall("ltm=(\\d*);",self.video_info)[0])
					lamtilo=int(re.findall('ltm=(\\d*);',self.video_info)[0])
				except:
					return(False,)
				if lamtilo==0:self.find_video()
				elif lamtilo>=1000:Write.Print(('</> Your IP was banned\n'),Colors.red_to_white,interval=0.001)
				_=time.time()
				while time.time()-2<_+lamtilo:
					t-=1
					print('[31m</> Vui lòng chờ: {0} '.format(t)+'giây .',end='\r')
					time.sleep(1)
				continue
			elif 'Too many requests. Please slow' in self.video_info:time.sleep(3)
			else:Write.Print((self.video_info),Colors.red_to_white,interval=0.001)
	def use_service(self):
		if self.find_video()[0]is False:return False
		self.token=''.join(random.choices(ascii_letters+digits,k=16))
		request=self.session.post(f'{self.base_url}{self.services_ids[self.service]}',headers={'content-type':f'multipart/form-data; boundary=----WebKitFormBoundary{self.token}','user-agent':self.headers['user-agent'],'origin':'https://zefoy.com'},data=f'------WebKitFormBoundary{self.token}\r\nContent-Disposition: form-data; name="{self.video_info[0]}"\r\n\r\n{self.video_info[1]}\r\n------WebKitFormBoundary{self.token}--\r\n')
		try:res=base64.b64decode(unquote(request.text.encode()[::-1])).decode()
		except:time.sleep(3); return ''
		if 'Session expired. Please re-login' in res:Write.Print(('</> Phiên hết hạn. Đang đăng nhập lại...\n'),Colors.red_to_white,interval=0.001);self.send_captcha(); return ''
		elif 'Too many requests. Please slow' in res:time.sleep(3)
		elif 'service is currently not working' in res:return('[Nguyên]</> Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.')
		else:print(res.split("sans-serif;text-align:center;color:green;'>")[1].split('</')[0])
	def get_video_info(self):
		request=self.session.get(f'https://tiktok.livecounts.io/video/stats/{urlparse(self.url).path.rpartition("/")[2]}',headers={'authority':'tiktok.livecounts.io','origin':'https://livecounts.io','user-agent':self.headers['user-agent']}).json()
		if 'likeCount' in request:return request
		else:return{'viewCount':0,'likeCount':0,'commentCount':0,'shareCount':0}
	def get_video_id(self,url_=None,set_url=True):
		if url_ is None:url_=self.url
		if url_[-1]=='/':url_=url_[:-1]
		url=urlparse(url_).path.rpartition('/')[2]
		if url.isdigit():self.url=url_; return url_
		request=requests.get(f'https://api.tokcount.com/?type=videoID&username=https://vm.tiktok.com/{url}',headers={'origin':'https://tokcount.com','authority':'api.tokcount.com','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
		if request.text=='':Write.Print(('</> Link video không hợ lệ\n'),Colors.red_to_white,interval=0.001); return False
		else:json_=request.json()
		if 'author' not in json_:Write.Print((f'{self.url}| Link video không hợp lệ\n'),Colors.red_to_white,interval=0.001); return False
		if set_url:self.url=f'https://www.tiktok.com/@{json_["author"]}/video/{json_["id"]}';Write.Print((f'Formated video url --> {self.url}'),Colors.red_to_white,interval=0.001)
		return request.text
	def check_config(self):
		while True:
			try:
				last_url=self.url
				if last_url !=self.url:self.get_video_id()
			except Exception as e:Write.Print((e),Colors.red_to_white,interval=0.001)
			time.sleep(4)
	def update_name(self):
		while True:
			try:
				ctypes.windll.kernel32.SetConsoleTitleA(self.text.encode())
				video_info=self.get_video_info()
				self.text=f"[hoàng tool]</> | Hearts: {like_info['likeCount']} "
			except:pass
			time.sleep(5)
trang='[1;37m'
xanh_la='[1;32m'
xanh_duong='[1;34m'
do='[1;31m'
vang='[1;33m'
tim='[1;35m'
dac_biet='[32;5;245m[1m[38;5;39m'
kt_code='</>'
from pystyle import Add,Center,Anime,Colors,Colorate,Write,System
System.Clear()
System.Title('Berserker')
System.Size(140,40)
banner='\n ███▄ ▄███▓ ██▓ ███▄    █  ██░ ██ ▄▄▄█████▓ ▒█████   ▒█████   ██▓      \n▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █ ▓██░ ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒      \n▓██    ▓██░▒██▒▓██  ▀█ ██▒▒██▀▀██░▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░      \n▒██    ▒██ ░██░▓██▒  ▐▌██▒░▓█ ░██ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      \n▒██▒   ░██▒░██░▒██░   ▓██░░▓█▒░██▓  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒  \n░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒  ▒ ░░▒░▒  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░  \n░  ░      ░ ▒ ░░ ░░   ░ ▒░ ▒ ░▒░ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░  \n░      ░    ▒ ░   ░   ░ ░  ░  ░░ ░  ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░     \n       ░    ░           ░  ░  ░  ░             ░ ░      ░ ░      ░  ░ \n                    ẤN ENTER ĐỂ VÀO TOOL'[1:]
Anime.Fade(Center.Center(banner),Colors.red_to_white,Colorate.Vertical,enter=True)
def logo():
    os.system('cls' if os.name=='nt' else 'clear')
    lg='\n                        .-/+osssso+/-`\n                   `/sdNMMMMMMMMMMMMMMNds/`\n                .odMMMMMMMMMMMMMMMMMMMMMMMMdo.\n              :hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh:\n            -dMMMNmMMMMMMMNNNNNNNNNNMMMMMMMmNMMMd-\n          `sMNNs-oMMMMNNNNNNNNNNNNNNNNNNMMMMo-sNNMs\n         `dM+s-:sMMMNNNNNNMMNMNNMNMMNNNNNNMMMs-:s+Md`\n        `mho.h/:dMNNMMMNMMNmNoso-dmNMMNMMMNNMd:/d`ohm`\n        hs//::oMMNMMMMNMMMMNMmmo+NNMMMMNMMMMNMNo:-+:yh\n       /M--y+:hMNNNNNNNMMMNNMMmmMMNMMMMNNNNNNNMh:oy.:M:\n       dd+./.hMNMMMMMNMMMNNNNNooNNNNNMMMNMMMMMNMy./.odh\n      `M-m-/yyMNMMMMMNMMMMNMNdssdNMNMMMMNMMMMMNMyy/-m-N\n      `M:-ho`NMNNNNNNNNNmho-sN:/Ms-shmNNNNNNNNNMm`sh-/M`\n      `Mh`+ sdMNMMMMMh`     NMosMN     `dMMMMMNMdo`/`hN\n       d/h/.m.MNMMMMM+      yM--My      oMMMMMNM.m`/h/h\n       /d`/ss mNNNNNN-      `d.-h`      -NNNNNNd ss/`d:\n        hm/`+ d:mNMMN                    NMMNd:h`+`/mh\n        `doss/++.mNNh                    hNNm`o//ssod`\n         `ds.:+y-:sso                    osy:-y+--sd`\n           sMy+/:./+                      +/.:/+yMs\n            -dyo/////.```            ```./////ohh-\n              :hMhoosss/`            `/sssoohMh:\n                .ohysoos.            .soosyh+`\n                   `/sdN`            `Nds/`\n         ...::::[ Tool by Tricker- Nguyen Minh ]::::...                  \n ███▄ ▄███▓ ██▓ ███▄    █  ██░ ██ ▄▄▄█████▓ ▒█████   ▒█████   ██▓      \n▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █ ▓██░ ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒      \n▓██    ▓██░▒██▒▓██  ▀█ ██▒▒██▀▀██░▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░      \n▒██    ▒██ ░██░▓██▒  ▐▌██▒░▓█ ░██ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      \n▒██▒   ░██▒░██░▒██░   ▓██░░▓█▒░██▓  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒  \n░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒  ▒ ░░▒░▒  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░  \n░  ░      ░ ▒ ░░ ░░   ░ ▒░ ▒ ░▒░ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░  \n░      ░    ▒ ░   ░   ░ ░  ░  ░░ ░  ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░     \n       ░    ░           ░  ░  ░  ░             ░ ░      ░ ░      ░  ░ \n ╔══════════════════════════════════════════════╗ \n   => TOOL Buff Tym Tiktok Zefoy\n   => Author: Tricker Nguyen Minh\n   => Zalo Admin: 0814463499\n ╚══════════════════════════════════════════════╝\n'
    from time import sleep
    Write.Print((lg),Colors.red_to_white,interval=0.0001)
from time import sleep  
logo()
# ngay=int(strftime('%d'))
# key1=str(ngay*24122006*241226)
# key='NDM'+key1
# key2='free'
# key3='Free'
# key4='FREE'
# url='https://deltagetkey.blogspot.com/2026/02/get-key.html?ma='+key
# token_link1s='6989d7bcd70a74263103abab'
# link1s=requests.get(f'https://link4m.co/api-shorten/v2?api={token}&url={url}').json()
# if link1s['status']=='error':
# 	Write.Print((link1s['message']),Colors.red_to_white,interval=0.001)
# 	quit()
# else:
# 	link_key=link1s['shortenedUrl']
# Write.Print(('</>Vì Miếng Cơm Nên Tui Mới Gắn Link Vượt Key\n</>Ae Thông Cảm Vượt Link Cho Tui Xíu Nha=]\n</>Key Sẽ Được Thay Đổi Theo Ngày\n'),Colors.red_to_white,interval=0.001)
# Write.Print((f"""┏Link Vượt Key: {link_key}\n"""),Colors.red_to_white,interval=0.001)
# keynhap=Write.Input(('┗━➤Key: '),Colors.red_to_white,interval=0.001)
# if keynhap==key:
#     Write.Print(('</> Đang Check Key...\n'),Colors.red_to_white,interval=0.001)
#     sleep(2)
#     Write.Print(('</> Key Đúng Mời Bạn Dùng Tool\n'),Colors.red_to_white,interval=0.001)
#     sleep(1.001)
# elif keynhap==key2 or keynhap==key3 or keynhap==key4:
#     Write.Print(('</> Đang Check Key...\n'),Colors.red_to_white,interval=0.001)
#     sleep(2)
#     Write.Print(('</> Key Đúng Mời Bạn Dùng Tool\n'),Colors.red_to_white,interval=0.001)
#     sleep(1.001)
# else:
#     Write.Print(('</> Đang Check Key...\n'),Colors.red_to_white,interval=0.001)
#     sleep(2)
#     Write.Print(('</> Key Sai Vui Lòng Vượt Link Lại'),Colors.red_to_white,interval=0.001)
#     quit()
os.system('cls' if os.name=='nt' else 'clear')
logo()
Z=Zefoy()
threading.Thread(target=Z.check_config).start()
threading.Thread(target=Z.update_name).start()
Z.send_captcha()
while True:
	try:
		if 'Service is currently not working, try again later' in str(Z.use_service()):print(f'{do}[Nguyên]</>Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.');time.sleep(5)
	except Exception as e:Write.Print((f'</>LỖI NGHIÊM TÚC | thử lại sau 10 giây.|| {e}\n'),Colors.red_to_white,interval=0.001);time.sleep(10)
