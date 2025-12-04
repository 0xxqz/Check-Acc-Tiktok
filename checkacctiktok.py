import requests
import json
import sys
from datetime import datetime
import textwrap

def format_number(num_str):
    """Format số với dấu phẩy cho dễ đọc"""
    if num_str == '-' or num_str == 'N/A':
        return num_str
    try:
        # Nếu đã có dấu phẩy thì giữ nguyên
        if ',' in num_str:
            return num_str
        # Nếu là số, thêm dấu phẩy
        num = int(num_str.replace(',', ''))
        return f"{num:,}"
    except:
        return num_str

def display_account_info(data):
    """Hiển thị thông tin tài khoản với format đẹp"""
    if data.get('status') != 'success':
        print(f"\n❌ Error: {data.get('message', 'Unknown error')}")
        return
    
    username = data.get('username', 'Unknown')
    stats = data.get('stats', {})
    details = data.get('details', {})
    timestamp = data.get('timestamp', '')
    
    # Format timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        formatted_time = timestamp
    
    print("\n" + "=" * 70)
    print("📱 TIKTOK ACCOUNT INFORMATION")
    print("=" * 70)
    
    # Basic Info
    print("\n📌 BASIC INFORMATION")
    print("-" * 40)
    print(f"   👤 Username:      @{username}")
    print(f"   🔑 User ID:       {details.get('user_id', 'N/A')}")
    print(f"   ⏰ Checked at:    {formatted_time}")
    
    # Statistics
    print("\n📊 STATISTICS")
    print("-" * 40)
    print(f"   👥 Followers:     {format_number(stats.get('followers', 'N/A'))}")
    print(f"   ↔️  Following:     {format_number(stats.get('following', 'N/A'))}")
    print(f"   ❤️  Hearts/Likes:  {format_number(stats.get('hearts', 'N/A'))}")
    print(f"   🎬 Videos:        {format_number(stats.get('videos', 'N/A'))}")
    print(f"   🤝 Friends:       {format_number(stats.get('friends', 'N/A'))}")
    
    # Tính ratio nếu có dữ liệu
    try:
        followers = int(stats.get('followers', '0').replace(',', ''))
        following = int(stats.get('following', '0').replace(',', ''))
        if following > 0:
            ratio = followers / following
            print(f"   📈 Follower/Following Ratio: {ratio:.2f}")
    except:
        pass
    
    # Account Details
    print("\n🔍 ACCOUNT DETAILS")
    print("-" * 40)
    print(f"   📅 Created:                {details.get('created', 'N/A')}")
    print(f"   ✏️  Nickname Edited At:     {details.get('modified', 'N/A')}")
    print(f"   🔄 Username Changed At:    {details.get('username_modified', 'N/A')}")
    
    # Summary
    print("\n📋 SUMMARY")
    print("-" * 40)
    
    # Đánh giá tài khoản dựa trên số followers
    try:
        followers = int(stats.get('followers', '0').replace(',', ''))
        if followers >= 10000000:
            print("   🏆 Level: Mega Celebrity (10M+ followers)")
        elif followers >= 1000000:
            print("   🌟 Level: Celebrity (1M+ followers)")
        elif followers >= 100000:
            print("   ⭐ Level: Influencer (100K+ followers)")
        elif followers >= 10000:
            print("   👍 Level: Micro-influencer (10K+ followers)")
        elif followers >= 1000:
            print("   👌 Level: Active User (1K+ followers)")
        else:
            print("   👤 Level: Regular User")
    except:
        print("   📊 Level: Unknown")
    
    # Hiển thị số liệu ấn tượng nhất
    max_stat = max([
        (stats.get('followers', '0'), 'Followers'),
        (stats.get('hearts', '0'), 'Likes'),
        (stats.get('videos', '0'), 'Videos')
    ], key=lambda x: int(x[0].replace(',', '')))
    
    print(f"   🏅 Most impressive: {format_number(max_stat[0])} {max_stat[1]}")
    
    print("\n" + "=" * 70)

def save_to_file(data, filename=None):
    """Lưu kết quả vào file JSON"""
    if not filename:
        username = data.get('username', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"tiktok_{username}_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def check_tiktok_account():
    """Function to input username and call API"""
    print("=" * 60)
    print("🔍 TIKTOK ACCOUNT CHECKER")
    print("=" * 60)
    
    # Get username from user
    print("\nEnter TikTok username (without @ symbol)")
    print("Examples: tiktok, khaby.lame, addisonre")
    username = input("\n👉 Username: ").strip()
    
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    # Remove @ symbol if present
    username = username.replace('@', '')
    
    print(f"\n🔍 Checking account: @{username}")
    print("⏳ Please wait... (This may take 10-20 seconds)")
    
    try:
        # Call API
        api_url = f"https://abc710b2176b.ngrok-free.app/api/?checktiktok={username}"
        response = requests.get(api_url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            # Hiển thị thông tin
            display_account_info(data)
            
            # Lưu kết quả
            if data.get('status') == 'success':
                filename = save_to_file(data)
                if filename:
                    print(f"\n💾 Results saved to: {filename}")
                
                # Hiển thị JSON raw (tùy chọn)
                show_raw = input("\n📋 Show raw JSON data? (y/n): ").strip().lower()
                if show_raw in ['y', 'yes']:
                    print("\n" + "-" * 40)
                    print("RAW JSON DATA:")
                    print("-" * 40)
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    
        else:
            print(f"\n❌ HTTP Error {response.status_code}: Cannot connect to server")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server. Make sure the server is running!")
        print("   Start server with: python server.py")
    except requests.exceptions.Timeout:
        print("\n❌ Timeout: Server took too long to respond")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

def print_welcome():
    """Hiển thị thông tin chào mừng"""
    print("✨" * 30)
    print(" " * 10 + "TIKTOK ACCOUNT ANALYZER")
    print("✨" * 30)
    
    print("\n📊 This tool will help you analyze any TikTok account")
    print("📈 Get detailed statistics and account information")
    print("\n📍 Features:")
    print("   • Followers, Following, Likes count")
    print("   • Account creation date")
    print("   • User ID (permanent identifier)")
    print("   • Account level analysis")
    print("   • JSON export")
    
    print("\n⚠️  Requirements:")
    print("   1. Server must be running (python server.py)")
    print("   2. Google Chrome must be installed")
    print("   3. Active internet connection")

def main():
    """Main function"""
    print_welcome()
    
    while True:
        check_tiktok_account()
        
        # Ask if user wants to continue
        print("\n" + "-" * 40)
        choice = input("\n🔄 Check another account? (y/n): ").strip().lower()
        if choice not in ['y', 'yes', 'có', 'co', '']:
            print("\n👋 Thank you for using TikTok Account Analyzer!")
            print("   Goodbye! 👋")
            break
        print("\n")

def check_dependencies():
    """Kiểm tra và cài đặt dependencies"""
    try:
        import requests
        from bs4 import BeautifulSoup
        from selenium import webdriver
        return True
    except ImportError:
        print("❌ Missing required libraries. Installing...")
        
        libraries = [
            "requests", 
            "beautifulsoup4", 
            "flask", 
            "flask-cors",
            "selenium",
            "webdriver-manager"
        ]
        
        try:
            import subprocess
            import sys
            
            for lib in libraries:
                print(f"📦 Installing {lib}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            
            print("\n✅ All libraries installed successfully!")
            print("⚠️  Please restart the program.")
            input("\nPress Enter to exit...")
            return False
            
        except Exception as e:
            print(f"❌ Error installing libraries: {e}")
            print("\n📋 Please install manually:")
            print("pip install requests beautifulsoup4 flask flask-cors selenium webdriver-manager")
            input("\nPress Enter to exit...")
            return False

if __name__ == "__main__":
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run main program
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        input("Press Enter to exit...")