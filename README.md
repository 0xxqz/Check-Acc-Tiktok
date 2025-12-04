TikTok Account Analyzer 🔍
Một công cụ phân tích thông tin tài khoản TikTok với giao diện API server và client.

📋 Tổng quan
Dự án này cung cấp hai phần chính:

Server API (server.py) - Backend Flask xử lý scraping thông tin TikTok

Client CLI (client.py) - Ứng dụng dòng lệnh để tương tác với API

🚀 Tính năng
Server API
✅ Lấy thông tin tài khoản TikTok (followers, following, likes, videos)

✅ Hỗ trợ cả phương pháp requests và Selenium

✅ API RESTful đơn giản với Flask

✅ CORS enabled cho phép truy cập từ nhiều nguồn

✅ Tự động khởi tạo Chrome Driver

✅ Xử lý lỗi chi tiết

Client CLI
✅ Giao diện dòng lệnh thân thiện

✅ Hiển thị thông tin được format đẹp

✅ Lưu kết quả vào file JSON

✅ Phân tích cấp độ tài khoản

✅ Kiểm tra dependencies tự động

✅ Hỗ trợ kiểm tra nhiều tài khoản liên tiếp

🛠️ Cài đặt
Yêu cầu hệ thống
Python 3.7+

Google Chrome (cho Selenium)

Internet connection

Cài đặt dependencies
bash
# Tự động cài đặt (chạy client lần đầu)
python client.py

# Hoặc cài đặt thủ công
pip install -r requirements.txt
requirements.txt
text
flask==2.3.3
flask-cors==4.0.0
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.0
webdriver-manager==4.0.1
📖 Hướng dẫn sử dụng
1. Khởi động Server
bash
python server.py
Server sẽ chạy tại: http://localhost:3000

Các endpoint:
GET / - Trang chủ với hướng dẫn

GET /api/?checktiktok=<username> - Lấy thông tin tài khoản

GET /health - Kiểm tra trạng thái server

2. Sử dụng Client
bash
python client.py
Sau đó nhập username TikTok cần kiểm tra.

3. Sử dụng trực tiếp API
bash
# Sử dụng curl
curl "http://localhost:3000/api/?checktiktok=tiktok"

# Hoặc truy cập trình duyệt
http://localhost:3000/api/?checktiktok=username
📊 Thông tin trả về
Response JSON
json
{
  "status": "success",
  "username": "tiktok",
  "timestamp": "2023-12-01T10:30:00",
  "stats": {
    "followers": "91,918,744",
    "following": "134",
    "hearts": "450,530,895",
    "videos": "34",
    "friends": "4"
  },
  "details": {
    "user_id": "107955",
    "created": "2020-03-01 12:00:00",
    "modified": "2022-05-15 10:30:00",
    "username_modified": "2021-08-20 14:25:00"
  }
}
🎯 Ví dụ sử dụng
Command Line
text
============================================================
🔍 TIKTOK ACCOUNT CHECKER
============================================================

Enter TikTok username (without @ symbol)
Examples: tiktok, khaby.lame, addisonre

👉 Username: tiktok

🔍 Checking account: @tiktok
⏳ Please wait... (This may take 10-20 seconds)

======================================================================
📱 TIKTOK ACCOUNT INFORMATION
======================================================================

📌 BASIC INFORMATION
----------------------------------------
   👤 Username:      @tiktok
   🔑 User ID:       107955
   ⏰ Checked at:    2023-12-01 10:30:00

📊 STATISTICS
----------------------------------------
   👥 Followers:     91,918,744
   ↔️  Following:     134
   ❤️  Hearts/Likes:  450,530,895
   🎬 Videos:        34
   🤝 Friends:       4

🔍 ACCOUNT DETAILS
----------------------------------------
   📅 Created:                2020-03-01 12:00:00
   ✏️  Nickname Edited At:     2022-05-15 10:30:00
   🔄 Username Changed At:    2021-08-20 14:25:00

📋 SUMMARY
----------------------------------------
   🏆 Level: Mega Celebrity (10M+ followers)
   🏅 Most impressive: 91,918,744 Followers

======================================================================
⚙️ Cấu hình
Server Configuration
Port mặc định: 3000

Timeout: 10-20 giây mỗi request

Headless Chrome để tối ưu hiệu suất

Tùy chỉnh port server
Sửa file server.py:

python
app.run(host='localhost', port=3000, debug=False)  # Thay đổi port tại đây
🐛 Xử lý lỗi
Lỗi thường gặp
"Cannot connect to server"

Kiểm tra server đã chạy chưa: python server.py

Kiểm tra firewall/port

"No TikTok information found"

Username không tồn tại

Website source thay đổi cấu trúc

Thử lại sau vài phút

"Failed to initialize browser"

Cài đặt Google Chrome

Kiểm tra Chrome Driver version

"Timeout error"

Mạng chậm

Server quá tải

Thử lại sau

Debug
Server lưu file debug: debug_screenshot.png, debug_page.html

Client lưu file JSON kết quả

Kiểm tra log terminal

----------------------------------
Chỉ cho mục đích giáo dục/phân tích

Không spam requests

Tôn trọng rate limits

Lưu ý
Dữ liệu được lấy từ public source

Có thể không chính xác 100%

Không chịu trách nhiệm cho việc sử dụng sai mục đích

🤝 Đóng góp
Fork repository

Tạo feature branch

Commit changes

Push to branch

Tạo Pull Request

📄 License
MIT License - Xem file LICENSE để biết chi tiết

Flask framework

Selenium WebDriver

BeautifulSoup4

📧 Liên hệ
Nếu có vấn đề hoặc câu hỏi:

Mở issue trên GitHub

Kiểm tra phần troubleshooting

Đọc kỹ documentation

⚠️ Lưu ý: Dự án này chỉ dành cho mục đích học tập và nghiên cứu. Tuân thủ các điều khoản sử dụng của TikTok và website liên quan.
