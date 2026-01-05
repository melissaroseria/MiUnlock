import webbrowser
webbrowser.open("t.me")
import subprocess
import sys
import os
import platform
import importlib

required_packages = ["requests", "ntplib", "pytz", "urllib3", "icmplib", "colorama", "linecache"]
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"{package} paketi kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

os.system('cls' if os.name == 'nt' else 'clear')
import requests, json, hashlib, base64, time
from urllib.parse import urlparse, parse_qs, quote
from colorama import init, Fore, Style
from getpass import getpass
col_y = Fore.YELLOW

def login():
    base_url = "https://account.xiaomi.com"
    sid = "18n_bbs_global"
    user_agent = "okhttp/4.12.0"
    headers = {"User-Agent": user_agent}
    def parse(res):
        return json.loads(res.text[11:])
    while True:
        cookies = {}
        user = input(f'{col_y} - Xiaomi Kullanıcı Adı: ')
        pwd = getpass(f'{col_y} - Şifre: ')
        hash_pwd = hashlib.md5(pwd.encode()).hexdigest().upper()
        try:
            r = requests.get(f"{base_url}/pass/serviceLogin", params={'sid': sid, '_json': True}, headers=headers, cookies=cookies)
            cookies.update(r.cookies.get_dict())
            data = {k: v[0] for k, v in parse_qs(urlparse(parse(r)['location']).query).items()}
            data.update({'user': user, 'hash': hash_pwd})
            r = requests.post(f"{base_url}/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)
            cookies.update(r.cookies.get_dict())
            res = parse(r)
            if res.get("code") == 70016:
                print("❌ Hatalı kullanıcı adı veya şifre. Lütfen tekrar deneyin.")
                time.sleep(0.7)
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            if 'notificationUrl' in res:
                print("⚠️ Hesap doğrulama gerekiyor (2FA etkin). Bu otomatik girişle mümkün değil.")
                time.sleep(0.7)
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            nonce, ssecurity = res['nonce'], res['ssecurity']
            client_sign = base64.b64encode(hashlib.sha1(f"nonce={nonce}&{ssecurity}".encode()).digest()).decode()
            res['location'] += f"&clientSign={quote(client_sign)}"
            final_cookies = requests.get(res['location'], headers=headers, cookies=cookies).cookies.get_dict()
            token = final_cookies.get("new_bbs_serviceToken")
            if token:
           #     print("✅ Giriş başarılı.")
                return token
            else:
                print("❌ Giriş başarısız. Tekrar deneyin.")
                time.sleep(0.7)
                os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            print(f"[Giriş hatası] {e}. Tekrar deneniyor.")
            time.sleep(0.7)
            os.system('cls' if os.name == 'nt' else 'clear')

token = login()  
cookie_value = token

while True:
    try:
        feedtime = float(input(f'{col_y} - Başvuru MS Gecikme (örnek: 500): '))
        break
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")

feed_time_shift = feedtime
feed_time_shift_1 = feed_time_shift / 1000
os.system('cls' if os.name == 'nt' else 'clear')

import hashlib
import random
import time
from datetime import datetime, timezone, timedelta
import ntplib
import pytz
import urllib3
from icmplib import ping
from colorama import init, Fore, Style


init(autoreset=True)
col_g = Fore.GREEN
col_gb = Style.BRIGHT + Fore.GREEN
col_b = Fore.BLUE
col_bb = Style.BRIGHT + Fore.BLUE
col_y = Fore.YELLOW
col_yb = Style.BRIGHT + Fore.YELLOW
col_r = Fore.RED
col_rb = Style.BRIGHT + Fore.RED


print(col_bb + "=" * 60 + Fore.RESET)
print(col_bb + "Senaryoyu geliştirmemize yardımcı olan Dgadg'a teşekkürler!" + Fore.RESET)
print(col_bb + "Düzenleme ve yeniden oluşturma: MIUI Türkiye Forum sitesi HiddeNKinG" + Fore.RESET)
print(col_bb + "=" * 60 + Fore.RESET)
print("")


ntp_servers = [
    "ntp0.ntp-servers.net", "ntp1.ntp-servers.net", "ntp2.ntp-servers.net",
    "ntp3.ntp-servers.net", "ntp4.ntp-servers.net", "ntp5.ntp-servers.net",
    "ntp6.ntp-servers.net"
]
MI_SERVERS = ['161.117.96.161', '20.157.18.26']

def generate_device_id():
    random_data = f"{random.random()}-{time.time()}"
    device_id = hashlib.sha1(random_data.encode('utf-8')).hexdigest().upper()
    return device_id


def get_initial_beijing_time():
    client = ntplib.NTPClient()
    beijing_tz = pytz.timezone("Asia/Shanghai")
    for server in ntp_servers:
        try:
            print(col_y + f"\nPekin'deki mevcut zaman belirleniyor" + Fore.RESET)
            response = client.request(server, version=3)
            ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
            beijing_time = ntp_time.astimezone(beijing_tz)
            print(col_g + f"[Pekin zamanı]: " + Fore.RESET + f"{beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            return beijing_time
        except Exception as e:
            print(f"{server} bağlantı hatası: {e}")
    print(f"Hiçbir NTP sunucusuna bağlanılamadı.")
    return None


def get_synchronized_beijing_time(start_beijing_time, start_timestamp):
    elapsed = time.time() - start_timestamp
    current_time = start_beijing_time + timedelta(seconds=elapsed)
    return current_time


def wait_until_target_time(start_beijing_time, start_timestamp):
    next_day = start_beijing_time + timedelta(days=1)
    print(col_y + f"\nBootloader kilit açma başvurusu yapılıyor" + Fore.RESET)
    print(col_g + f"[Belirtilen gecikme]: " + Fore.RESET + f"{feed_time_shift:.2f} ms.")
    target_time = next_day.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=feed_time_shift_1)
    print(col_g + f"[Bekleniyor]: " + Fore.RESET + f"{target_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"Lütfen pencereyi kapatmayın...")

    while True:
        current_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        time_diff = target_time - current_time

        if time_diff.total_seconds() > 1:
            time.sleep(min(1.0, time_diff.total_seconds() - 1))
        elif current_time >= target_time:
            print(f"Zaman ulaşıldı: {current_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. İstek gönderiliyor...")
            break
        else:
            time.sleep(0.0001)


def check_unlock_status(session, cookie_value, device_id):
    try:
        url = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }
        response = session.make_request('GET', url, headers=headers)
        if response is None:
            print(f"[Hata] Kilit açma durumu alınamadı.")
            return False

        response_data = json.loads(response.data.decode('utf-8'))
        response.release_conn()

        if response_data.get("code") == 100004:
            print(f"[Hata] Cookie süresi doldu, güncellenmesi gerekiyor!")
            input(f"Kapatmak için Enter tuşuna basın...")
            exit()

        data = response_data.get("data", {})
        is_pass = data.get("is_pass")
        button_state = data.get("button_state")
        deadline_format = data.get("deadline_format", "")

        if is_pass == 4:
            if button_state == 1:
                    print(col_g + f"[Hesap durumu]: " + Fore.RESET + f"başvuru yapılabilir.")
                    return True

            elif button_state == 2:
                print(col_g + f"[Hesap durumu]: " + Fore.RESET + f"başvuru engeli {deadline_format} (Ay/Gün) tarihine kadar.")
                status_2 = (input(f"Devam etmek ister misiniz (" + col_b + f"Evet/Hayır" + Fore.RESET + f")?: "))
                if status_2.lower() in ['e', 'evet', 'y', 'yes']:
                    return True
                else:
                    input(f"Kapatmak için Enter tuşuna basın...")
                    exit()
            elif button_state == 3:
                print(col_g + f"[Hesap durumu]: " + Fore.RESET + f"hesap 30 günden daha yeni oluşturulmuş.")
                status_3 = (input(f"Devam etmek ister misiniz (" + col_b + f"Evet/Hayır" + Fore.RESET + f")?: "))
                if status_3.lower() in ['e', 'evet', 'y', 'yes']:
                    return True
                else:
                    input(f"Kapatmak için Enter tuşuna basın...")
                    exit()
        elif is_pass == 1:
            print(col_g + f"[Hesap durumu]: " + Fore.RESET + f"başvuru onaylandı, {deadline_format} tarihine kadar kilit açılabilir.")
            input(f"Kapatmak için Enter tuşuna basın...")
            exit()
        else:
            print(col_g + f"[Hesap durumu]: " + Fore.RESET + f"bilinmeyen durum.")
            input(f"Kapatmak için Enter tuşuna basın...")
            exit()
    except Exception as e:
        print(f"[Durum kontrol hatası] {e}")
        return False


class HTTP11Session:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=10,
            retries=True,
            timeout=urllib3.Timeout(connect=2.0, read=15.0),
            headers={}
        )

    def make_request(self, method, url, headers=None, body=None):
        try:
            request_headers = {}
            if headers:
                request_headers.update(headers)
                request_headers['Content-Type'] = 'application/json; charset=utf-8'
            
            if method == 'POST':
                if body is None:
                    body = '{"is_retry":true}'.encode('utf-8')
                request_headers['Content-Length'] = str(len(body))
                request_headers['Accept-Encoding'] = 'gzip, deflate, br'
                request_headers['User-Agent'] = 'okhttp/4.12.0'
                request_headers['Connection'] = 'keep-alive'
            
            response = self.http.request(
                method,
                url,
                headers=request_headers,
                body=body,
                preload_content=False
            )
            
            return response
        except Exception as e:
            print(f"[Ağ hatası] {e}")
            return None


def main():
    device_id = generate_device_id()
    session = HTTP11Session()

    if check_unlock_status(session, cookie_value, device_id):
        start_beijing_time = get_initial_beijing_time()
        if start_beijing_time is None:
            print(f"Başlangıç zamanı belirlenemedi. Kapatmak için Enter tuşuna basın...")
            input()
            exit()

        start_timestamp = time.time()
        wait_until_target_time(start_beijing_time, start_timestamp)

        url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }

        try:
            while True:
                request_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[İstek]: " + Fore.RESET + f"{request_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8) zamanında istek gönderiliyor")
                
                response = session.make_request('POST', url, headers=headers)
                if response is None:
                    continue

                response_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[Yanıt]: " + Fore.RESET + f"{response_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8) zamanında yanıt alındı")

                try:
                    response_data = response.data
                    response.release_conn()
                    json_response = json.loads(response_data.decode('utf-8'))
                    code = json_response.get("code")
                    data = json_response.get("data", {})

                    if code == 0:
                        apply_result = data.get("apply_result")
                        if apply_result == 1:
                            print(col_g + f"[Durum]: " + Fore.RESET + f"Başvuru onaylandı, durum kontrol ediliyor...")
                            check_unlock_status(session, cookie_value, device_id)
                        elif apply_result == 3:
                            deadline_format = data.get("deadline_format", "Belirtilmemiş")
                            print(col_g + f"[Durum]: " + Fore.RESET + f"Başvuru yapılamadı, başvuru limiti aşıldı, {deadline_format} (Ay/Gün) tarihinde tekrar deneyin.")
                            input(f"Kapatmak için Enter tuşuna basın...")
                            exit()
                        elif apply_result == 4:
                            deadline_format = data.get("deadline_format", "Belirtilmemiş")
                            print(col_g + f"[Durum]: " + Fore.RESET + f"Başvuru yapılamadı, {deadline_format} (Ay/Gün) tarihine kadar başvuru engeli var.")
                            input(f"Kapatmak için Enter tuşuna basın...")
                            exit()
                    elif code == 100001:
                        print(col_g + f"[Durum]: " + Fore.RESET + f"Başvuru reddedildi, istek hatası.")
                        print(col_g + f"[TAM YANIT]: " + Fore.RESET + f"{json_response}")
                    elif code == 100003:
                        print(col_g + f"[Durum]: " + Fore.RESET + f"Başvuru muhtemelen onaylandı, durum kontrol ediliyor...")
                        print(col_g + f"[Tam yanıt]: " + Fore.RESET + f"{json_response}")
                        check_unlock_status(session, cookie_value, device_id)
                    elif code is not None:
                        print(col_g + f"[Durum]: " + Fore.RESET + f"Bilinmeyen başvuru durumu: {code}")
                        print(col_g + f"[Tam yanıt]: " + Fore.RESET + f"{json_response}")
                    else:
                        print(col_g + f"[Hata]: " + Fore.RESET + f"Yanıt gerekli kodu içermiyor.")
                        print(col_g + f"[Tam yanıt]: " + Fore.RESET + f"{json_response}")

                except json.JSONDecodeError:
                    print(col_g + f"[Hata]: " + Fore.RESET + f"JSON yanıtı çözümlenemedi.")
                    print(col_g + f"[Sunucu yanıtı]: " + Fore.RESET + f"{response_data}")
                except Exception as e:
                    print(col_g + f"[Yanıt işleme hatası]: " + Fore.RESET + f"{e}")
                    continue

        except Exception as e:
            print(col_g + f"[İstek hatası]: " + Fore.RESET + f"{e}")
            input(f"Kapatmak için Enter tuşuna basın...")
            exit()

if __name__ == "__main__":

    main()
