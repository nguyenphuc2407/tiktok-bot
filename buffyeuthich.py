#!/usr/bin/python3
# NPNDecode:)

import os
try:
	import requests,colorama,prettytable
except:
	os.system("pip install requests")
	os.system("pip install colorama")
	os.system("pip install prettytable")
import threading, requests, ctypes, random, json, time, base64, sys, re
from prettytable import PrettyTable
import random
from time import strftime
from colorama import init, Fore
from urllib.parse import urlparse, unquote, quote
from string import ascii_letters, digits

class Zefoy:
	# if os.path.exists('config.json') is False: open('config.json','w',encoding='utf-8',errors='ignore').write(json.dumps({'url':'https://www.tiktok.com/t/ZTRToxYct','service':'Favorites'},indent=4))

	def __init__(self):
		self.base_url = 'https://zefoy.com/'
		self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
		self.session = requests.Session()
		self.captcha_1 = None
		self.captcha_ = {}
		self.service = 'Favorites'
		self.video_key = None
		self.services = {}
		self.services_ids = {}
		self.services_status = {}
		self.url = 'None'
		self.text = 'Nguyên'
		url1=input("[Nguyên]</> Nhập link video: ")
		self.url=url1

	def get_captcha(self):
		if os.path.exists('session'): self.session.cookies.set("PHPSESSID", open('session',encoding='utf-8').read(), domain='zefoy.com')
		request = self.session.get(self.base_url, headers=self.headers)
		if 'Enter Video URL' in request.text: self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]; return True

		try:
			for x in re.findall(r'<input type="hidden" name="(.*)" value="(.*)">', request.text): self.captcha_[x[0]] = x[1]

			self.captcha_1 = request.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
			captcha_url = request.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0]
			request = self.session.get(f"{self.base_url}{captcha_url}",headers=self.headers)
			open('captcha.png', 'wb').write(request.content)
			print('[Nguyên]</> Đang giải capcha..')
			return False
		except Exception as e:
			print(f"[Nguyên]</> Không thể giải captcha: {e}")
			time.sleep(2)
			self.get_captcha()

	def send_captcha(self, new_session = False):
		if new_session: self.session = requests.Session(); os.remove('session'); time.sleep(2)
		if self.get_captcha(): print('[Nguyên]</> Đang kêt nối đến session');return (True, 'The session already exists')
		captcha_solve = self.solve_captcha('captcha.png')[1]
		self.captcha_[self.captcha_1] = captcha_solve
		request = self.session.post(self.base_url, headers=self.headers, data=self.captcha_)

		if 'Enter Video URL' in request.text: 
			print('[Nguyên]</> Session đã được tạo')
			open('session','w',encoding='utf-8').write(self.session.cookies.get('PHPSESSID'))
			print(f"[Nguyên]</> Giải capcha thành công: {captcha_solve}")
			self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
			return (True,captcha_solve)
		else: return (False,captcha_solve)

	def solve_captcha(self, path_to_file = None, b64 = None, delete_tag = ['\n','\r']):
		if path_to_file: task = path_to_file
		else: open('temp.png','wb').write(base64.b64decode(b64)); task = 'temp.png'
		request = self.session.post('https://api.ocr.space/parse/image?K87899142388957', headers={'apikey':'K87899142388957'}, files={'task':open(task,'rb')}).json()
		solved_text = request['ParsedResults'][0]['ParsedText']
		for x in delete_tag: solved_text = solved_text.replace(x,'')
		return (True, solved_text)

	def get_status_services(self):
		request = self.session.get(self.base_url, headers=self.headers).text
		for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', request): self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
		for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', request): self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
		for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+<button .+', request): self.services_status[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = False if 'disabled class' in x else True
		return (self.services, self.services_status)

	def get_table(self, i = 1):
		table = PrettyTable(field_names=["ID", "DỊCH VỤ", "Status"], title="Status Services", header_style="upper",border=True)
		while True:
			if len(self.get_status_services()[0])>1:break
			else:print('Cant get services, retrying...');self.send_captcha();time.sleep(2)
		for service in self.services: table.add_row([f"{Fore.CYAN}{i}{Fore.RESET}", service, f"{Fore.GREEN if 'ago updated' in self.services[service] else Fore.RED}{self.services[service]}{Fore.RESET}"]); i+=1
		table.title =  f"{Fore.YELLOW}Số Dịch Vụ Hoạt Động: {len([x for x in self.services_status if self.services_status[x]])}{Fore.RESET}"
		print(table)

	def find_video(self):
		if self.service is None: return (False, "You didn't choose the service")
		while True:
			if self.service not in self.services_ids: self.get_status_services(); time.sleep(1)
			request = self.session.post(f'{self.base_url}{self.services_ids[self.service]}', headers={'content-type':'multipart/form-data; boundary=----WebKitFormBoundary0nU8PjANC8BhQgjZ', 'user-agent':self.headers['user-agent'], 'origin':'https://zefoy.com'}, data=f'------WebKitFormBoundary0nU8PjANC8BhQgjZ\r\nContent-Disposition: form-data; name="{self.video_key}"\r\n\r\n{self.url}\r\n------WebKitFormBoundary0nU8PjANC8BhQgjZ--\r\n')
			try: self.video_info = base64.b64decode(unquote(request.text.encode()[::-1])).decode()
			except: time.sleep(3); continue
			if 'Session expired. Please re-login' in self.video_info: print('[Nguyên]</> Phiên hết hạn. Đang đăng nhập lại...');self.send_captcha(); return
			elif 'service is currently not working' in self.video_info: return (True,'[Nguyên]</> Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.')
			elif """onsubmit="showHideElements""" in self.video_info:
				self.video_info = [self.video_info.split('" name="')[1].split('"')[0],self.video_info.split('value="')[1].split('"')[0]]
				return (True, request.text)
			elif 'Checking Timer...' in self.video_info:
				try: 
					t=int(re.findall(r'ltm=(\d*);', self.video_info)[0])
					nguyendz = int(re.findall(r'ltm=(\d*);', self.video_info)[0])
				except: 
					return (False,)
				if nguyendz==0:self.find_video()
				elif nguyendz >= 1000: print('[Nguyên]</> Your IP was banned')
				# print(f'[Nguyên]</> Thời gian chờ để tiếp tục tăng: {t} giây')
				# for nguyen in range(t,0,-1):
				# 	nguyen-=1
				# 	print(f"[Nguyên]</> Vui lòng chờ: {nguyen}",end="\r")
				# 	time.sleep(1)
				_=time.time()
				while time.time()-2<_+nguyendz:
					t-=1
					print("[Nguyên]</> Vui lòng chờ: {0} ".format(t)+"giây .", end="\r")
					time.sleep(1)
					
				continue
			elif 'Too many requests. Please slow' in self.video_info: time.sleep(3)
			else: print(self.video_info)

	def use_service(self):
		if self.find_video()[0] is False: return False
		self.token = "".join(random.choices(ascii_letters+digits, k=16))
		request = self.session.post(f'{self.base_url}{self.services_ids[self.service]}', headers={'content-type':f'multipart/form-data; boundary=----WebKitFormBoundary{self.token}', 'user-agent':self.headers['user-agent'], 'origin':'https://zefoy.com'}, data=f'------WebKitFormBoundary{self.token}\r\nContent-Disposition: form-data; name="{self.video_info[0]}"\r\n\r\n{self.video_info[1]}\r\n------WebKitFormBoundary{self.token}--\r\n')
		try: res = base64.b64decode(unquote(request.text.encode()[::-1])).decode()
		except: time.sleep(3); return ""
		if 'Session expired. Please re-login' in res: print('[Nguyên]</> Phiên hết hạn. Đang đăng nhập lại...');self.send_captcha(); return ""
		elif 'Too many requests. Please slow' in res: time.sleep(3)
		elif 'service is currently not working' in res: return ('[Nguyên]</> Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.')
		else: print(res.split("sans-serif;text-align:center;color:green;'>")[1].split("</")[0])

	def get_video_info(self):
		request = self.session.get(f'https://tiktok.livecounts.io/video/stats/{urlparse(self.url).path.rpartition("/")[2]}',headers={'authority':'tiktok.livecounts.io','origin':'https://livecounts.io','user-agent':self.headers['user-agent']}).json()
		if 'viewCount' in request: return request
		else: return {'viewCount':0, 'likeCount':0,'commentCount':0,'shareCount':0}

	def get_video_id(self, url_ = None, set_url=True):
		if url_ is None: url_ = self.url
		if url_[-1] == '/': url_=url_[:-1]
		url = urlparse(url_).path.rpartition('/')[2]
		if url.isdigit(): self.url = url_; return url_
		request = requests.get(f'https://api.tokcount.com/?type=videoID&username=https://vm.tiktok.com/{url}',headers={'origin': 'https://tokcount.com','authority': 'api.tokcount.com','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})
		if request.text == '': print('[Nguyên]</> Link video không hợ lệ'); return False
		else: json_=request.json()
		if 'author' not in json_: print(f'{self.url}| Link video không hợp lệ'); return False
		if set_url: self.url = f'https://www.tiktok.com/@{json_["author"]}/video/{json_["id"]}';print(f'Formated video url --> {self.url}')
		return request.text

	def check_config(self):
		
		while True:
			try: 
				last_url = self.url
				if last_url != self.url: self.get_video_id()
			except Exception as e: print(e)
			time.sleep(4)
	def update_name(self):
		while True:
			try:
				ctypes.windll.kernel32.SetConsoleTitleA(self.text.encode())
				video_info = self.get_video_info()
				self.text = f"[Nguyên]</> | Views: {video_info['viewCount']} "
			except: pass
			time.sleep(5)
trang = "\033[1;37m"
xanh_la = "\033[1;32m"
xanh_duong = "\033[1;34m"
do = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
dac_biet = "\033[32;5;245m\033[1m\033[38;5;39m"
kt_code = "</>"
def logo():
    os.system("cls" if os.name == "nt" else "clear")
    trang = "\033[1;37m"
    xanh_la = "\033[1;32m"
    xanh_duong = "\033[1;34m"
    do = "\033[1;31m"
    vang = "\033[1;33m"
    tim = "\033[1;35m"
    dac_biet = "\033[32;5;245m\033[1m\033[38;5;39m"
    kt_code = "</>"
    logo=f"""

    \033[1;37m────────────────────────────────────────────────────────────
    {do}[{trang}{kt_code}{do}] {vang}TOOL BUFF TYM TIKTOK 
    {do}[{trang}{kt_code}{do}] \033[1;35mADMIN:\033[1;36m Nguyễn Phúc Nguyên
    {do}[{trang}{kt_code}{do}] {dac_biet}YOUTUBE:\033[1;37m NPN Decode:)
    \033[1;37m────────────────────────────────────────────────────────────\n"""
  
    print(logo)


if 1:
    logo()
    Z = Zefoy()
    threading.Thread(target=Z.check_config).start()
    threading.Thread(target=Z.update_name).start()
    # time.sleep(5)
    Z.send_captcha()
    Z.get_table()
else:
    print(f"{do}[Nguyên]</> Key sai vui lòng vượt lại")
    exit()

while True:
	try: 
		if 'Service is currently not working, try again later' in str(Z.use_service()): print(f'{do}[LÂMTILO]</>Dịch vụ hiện không hoạt động, hãy thử lại sau. | Bạn có thể thay đổi nó trong cấu hình.');time.sleep(5)
	except Exception as e:print(f'LỖI NGHIÊM TÚC | thử lại sau 10 giây.|| {e}');time.sleep(10)