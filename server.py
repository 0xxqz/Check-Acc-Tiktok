from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading

app = Flask(__name__)
CORS(app)

# Biến toàn cục để lưu driver
driver = None
driver_lock = threading.Lock()

def init_driver():
    """Khởi tạo Chrome driver"""
    global driver
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Chạy ẩn
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Tắt logging
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.implicitly_wait(10)
        return True
    except Exception as e:
        print(f"Error initializing driver: {e}")
        return False

def scrape_tiktok_info_selenium(username):
    """Scrape thông tin bằng Selenium"""
    global driver
    
    try:
        with driver_lock:
            if not driver:
                if not init_driver():
                    return {"status": "error", "message": "Failed to initialize browser"}
            
            # Truy cập trang web
            url = "https://omar-thing.site/"
            print(f"Navigating to: {url}")
            driver.get(url)
            time.sleep(2)
            
            # Tìm input field
            try:
                # Thử nhiều cách tìm input field
                input_selectors = [
                    'input#usernameInput',
                    'input[placeholder*="TikTok username"]',
                    'input[placeholder*="Enter TikTok"]',
                    'input[type="text"]',
                    '.input-group input',
                    'input'
                ]
                
                input_field = None
                for selector in input_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            placeholder = element.get_attribute('placeholder') or ''
                            if 'tiktok' in placeholder.lower() or 'username' in placeholder.lower():
                                input_field = element
                                break
                        if input_field:
                            break
                    except:
                        continue
                
                if not input_field:
                    # Chụp ảnh màn hình để debug
                    driver.save_screenshot('debug_screenshot.png')
                    html = driver.page_source
                    with open('debug_page.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    
                    return {"status": "error", "message": "Cannot find username input field"}
                
                # Nhập username
                input_field.clear()
                input_field.send_keys(username)
                time.sleep(1)
                
                # Tìm và click nút search
                button_selectors = [
                    'button#fetchButton',
                    'button[aria-label*="Fetch"]',
                    'button[aria-label*="Search"]',
                    'button:contains("Fetch")',
                    '.input-group button',
                    'button'
                ]
                
                search_button = None
                for selector in button_selectors:
                    try:
                        if 'contains' in selector:
                            # Tìm bằng text
                            buttons = driver.find_elements(By.TAG_NAME, 'button')
                            for button in buttons:
                                text = button.text.lower()
                                if 'fetch' in text or 'search' in text:
                                    search_button = button
                                    break
                        else:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            for element in elements:
                                aria_label = element.get_attribute('aria-label') or ''
                                text = element.text.lower()
                                if 'fetch' in aria_label.lower() or 'search' in aria_label.lower() or 'fetch' in text:
                                    search_button = element
                                    break
                        if search_button:
                            break
                    except:
                        continue
                
                if search_button:
                    search_button.click()
                else:
                    # Thử nhấn Enter
                    input_field.send_keys(Keys.RETURN)
                
                # Chờ kết quả load
                time.sleep(3)
                
                # Lấy page source
                page_source = driver.page_source
                
                # Lưu để debug
                with open(f'selenium_result_{username}.html', 'w', encoding='utf-8') as f:
                    f.write(page_source)
                
                # Parse HTML
                soup = BeautifulSoup(page_source, 'html.parser')
                
            except Exception as e:
                return {"status": "error", "message": f"Selenium error: {str(e)}"}
        
        # Parse thông tin từ HTML
        return parse_tiktok_info(soup, username)
        
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

def parse_tiktok_info(soup, username):
    """Parse thông tin từ HTML"""
    stats = {
        'following': '-',
        'followers': '-',
        'hearts': '-',
        'videos': '-',
        'friends': '-'
    }
    
    details = {
        'user_id': '-',
        'created': '-',
        'modified': '-',
        'username_modified': '-'
    }
    
    # Tìm theo ID (từ ảnh)
    stat_ids = {
        'statFollowing': 'following',
        'statFollowers': 'followers',
        'statHearts': 'hearts',
        'statVideos': 'videos',
        'statFriends': 'friends'
    }
    
    for element_id, stat_key in stat_ids.items():
        element = soup.find('span', {'id': element_id})
        if element:
            stats[stat_key] = element.get_text(strip=True)
    
    # Tìm details theo ID
    detail_ids = {
        'resultUserId': 'user_id',
        'resultCreated': 'created',
        'resultModified': 'modified',
        'resultUsernameModified': 'username_modified'
    }
    
    for element_id, detail_key in detail_ids.items():
        element = soup.find('strong', {'id': element_id})
        if element:
            details[detail_key] = element.get_text(strip=True)
    
    # Nếu không tìm thấy bằng ID, thử tìm bằng regex
    all_text = soup.get_text()
    
    # Tìm followers (ví dụ: "91,918,744 Followers")
    followers_match = re.search(r'(\d[\d,]*)\s*Followers?', all_text, re.IGNORECASE)
    if followers_match and stats['followers'] == '-':
        stats['followers'] = followers_match.group(1)
    
    # Tìm hearts (ví dụ: "450,530,895 Hearts")
    hearts_match = re.search(r'(\d[\d,]*)\s*Hearts?', all_text, re.IGNORECASE)
    if hearts_match and stats['hearts'] == '-':
        stats['hearts'] = hearts_match.group(1)
    
    # Tìm friends (ví dụ: "4 Friends")
    friends_match = re.search(r'(\d[\d,]*)\s*Friends?', all_text, re.IGNORECASE)
    if friends_match and stats['friends'] == '-':
        stats['friends'] = friends_match.group(1)
    
    # Tìm User ID
    user_id_match = re.search(r'User ID:\s*(\d+)', all_text, re.IGNORECASE)
    if user_id_match and details['user_id'] == '-':
        details['user_id'] = user_id_match.group(1)
    
    # Tìm Created date
    created_match = re.search(r'Created:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', all_text, re.IGNORECASE)
    if created_match and details['created'] == '-':
        details['created'] = created_match.group(1)
    
    # Tìm thông tin trong các phần tử có class
    # Tìm các số lớn có thể là stats
    large_numbers = re.findall(r'>(\d{1,3}(?:,\d{3})+)<', str(soup))
    if large_numbers:
        if len(large_numbers) >= 1 and stats['followers'] == '-':
            stats['followers'] = large_numbers[0]
        if len(large_numbers) >= 2 and stats['hearts'] == '-':
            stats['hearts'] = large_numbers[1]
    
    # Tìm trong các thẻ strong
    for strong_tag in soup.find_all('strong'):
        text = strong_tag.get_text(strip=True)
        parent = strong_tag.parent
        if parent:
            parent_text = parent.get_text()
            if 'User ID:' in parent_text and details['user_id'] == '-':
                details['user_id'] = text
            elif 'Created:' in parent_text and details['created'] == '-':
                details['created'] = text
            elif 'Nickname Edited At:' in parent_text and details['modified'] == '-':
                details['resultModified'] = text
            elif 'Username Changed At:' in parent_text and details['username_modified'] == '-':
                details['resultUsernameModifiedP'] = text
    
    # Kiểm tra xem có tìm thấy thông tin không
    if (all(v == '-' for v in stats.values()) and 
        all(v == '-' for v in details.values())):
        return {
            "status": "error",
            "message": "No TikTok information found. The account may not exist or website structure changed.",
            "username": username
        }
    
    return {
        'status': 'success',
        'username': username,
        'stats': stats,
        'details': details,
        'timestamp': datetime.now().isoformat()
    }

def scrape_tiktok_info_requests(username):
    """Thử phương pháp requests đơn giản hơn"""
    try:
        # Thử truy cập trực tiếp với username trong URL
        url = f"https://omar-thing.site/?username={username}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return parse_tiktok_info(soup, username)
        else:
            return {"status": "error", "message": f"HTTP Error {response.status_code}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Requests error: {str(e)}"}

@app.route('/api/', methods=['GET'])
def check_tiktok():
    """API endpoint để kiểm tra thông tin TikTok"""
    username = request.args.get('checktiktok')
    
    if not username:
        return jsonify({
            'status': 'error',
            'message': 'Missing username parameter. Use: /api/?checktiktok=<username>'
        }), 400
    
    # Xóa @ nếu có
    username = username.replace('@', '').strip()
    
    print(f"Checking TikTok account: {username}")
    
    # Thử phương pháp đơn giản trước
    result = scrape_tiktok_info_requests(username)
    
    # Nếu không thành công, thử Selenium
    if result.get('status') != 'success':
        print("Trying Selenium method...")
        result = scrape_tiktok_info_selenium(username)
    
    return jsonify(result)

@app.route('/')
def index():
    return jsonify({
        'message': 'TikTok Checker API',
        'usage': 'Use /api/?checktiktok=<username> to check TikTok information',
        'example': 'http://localhost:3000/api/?checktiktok=tiktok',
        'methods': 'Uses both requests and Selenium for maximum compatibility'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'})

if __name__ == '__main__':
    # Khởi tạo Selenium driver khi start
    init_thread = threading.Thread(target=init_driver)
    init_thread.start()
    
    app.run(host='localhost', port=3000, debug=False)