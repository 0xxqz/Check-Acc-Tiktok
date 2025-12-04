TikTok Account Analyzer 🔍
https://img.shields.io/badge/Python-3.7+-blue.svg
https://img.shields.io/badge/Flask-2.3.3-green.svg
https://img.shields.io/badge/Selenium-4.15.0-orange.svg
https://img.shields.io/badge/License-MIT-yellow.svg

Một công cụ phân tích thông tin tài khoản TikTok với API server và giao diện dòng lệnh. Hỗ trợ lấy thông tin chi tiết từ các tài khoản TikTok công khai.

✨ Tính năng nổi bật
📊 Lấy thông tin chi tiết: Followers, Following, Likes, Videos, Friends

🔍 Thông tin tài khoản: User ID, ngày tạo, lịch sử chỉnh sửa

⚡ Hỗ trợ đa phương pháp: Requests + Selenium cho độ tin cậy cao

🎨 Giao diện CLI đẹp: Hiển thị thông tin với emoji và formatting

💾 Xuất file JSON: Tự động lưu kết quả phân tích

📈 Phân tích cấp độ: Đánh giá mức độ nổi tiếng của tài khoản

🔄 Kiểm tra liên tục: Hỗ trợ check nhiều tài khoản không giới hạn

📋 Mục lục
Cài đặt

Cách sử dụng

API Documentation

Ví dụ

Cấu trúc project

Xử lý lỗi

Đóng góp

Giấy phép

🚀 Cài đặt
Yêu cầu hệ thống
Python 3.7 trở lên

Google Chrome (cho Selenium WebDriver)

Kết nối Internet

Cài đặt tự động
bash
# Clone repository
git clone https://github.com/yourusername/tiktok-analyzer.git
cd tiktok-analyzer

# Chạy client để tự động cài đặt dependencies
python client.py
Cài đặt thủ công
bash
# Clone repository
git clone https://github.com/yourusername/tiktok-analyzer.git
cd tiktok-analyzer

# Cài đặt dependencies
pip install -r requirements.txt
requirements.txt
text
flask==2.3.3
flask-cors==4.0.0
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.0
webdriver-manager==4.0.1
🎮 Cách sử dụng
1. Khởi động Server
bash
# Chạy server (port mặc định: 3000)
python server.py

# Hoặc chạy trên port khác
python server.py --port 8080
Server sẽ khởi động tại: http://localhost:3000

2. Sử dụng Client (CLI)
bash
# Chạy client
python client.py
3. Sử dụng trực tiếp qua API
bash
# Sử dụng curl
curl "http://localhost:3000/api/?checktiktok=tiktok"

# Hoặc mở trình duyệt
http://localhost:3000/api/?checktiktok=username
📖 API Documentation
Endpoints
GET /
Trang chủ với thông tin hướng dẫn sử dụng API.

Response:

json
{
  "message": "TikTok Checker API",
  "usage": "Use /api/?checktiktok=<username> to check TikTok information",
  "example": "http://localhost:3000/api/?checktiktok=tiktok",
  "methods": "Uses both requests and Selenium for maximum compatibility"
}
GET /api/?checktiktok=<username>
Lấy thông tin tài khoản TikTok.

Parameters:

checktiktok (required): Username TikTok (không cần @)

Example Request:

http
GET /api/?checktiktok=tiktok
Example Response:

json
{
  "status": "success",
  "username": "tiktok",
  "timestamp": "2023-12-01T10:30:00.000Z",
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
GET /health
Kiểm tra trạng thái server.

Response:

json
{
  "status": "ok",
  "message": "API is running"
}
📊 Ví dụ
Giao diện CLI
text
✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
          TIKTOK ACCOUNT ANALYZER
✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨

🔍 Enter TikTok username: tiktok

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
   📈 Follower/Following Ratio: 685,960.78

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
💾 Results saved to: tiktok_tiktok_20231201_103000.json
File JSON Output
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
📁 Cấu trúc project
text
tiktok-analyzer/
│
├── server.py              # Backend Flask API server
├── client.py              # Frontend CLI application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation (bạn đang đọc)
├── LICENSE               # MIT License file
│
├── debug_screenshot.png  # Debug screenshot (tạo tự động)
├── debug_page.html       # Debug HTML page (tạo tự động)
├── selenium_result_*.html# Selenium results (tạo tự động)
│
└── tiktok_*.json         # JSON output files (tạo tự động)
Chi tiết file
server.py: Flask server với Selenium WebDriver

client.py: Giao diện dòng lệnh tương tác với API

requirements.txt: Danh sách thư viện Python cần thiết

🔧 Xử lý lỗi
Lỗi thường gặp
Lỗi	Nguyên nhân	Giải pháp
Cannot connect to server	Server chưa chạy	Chạy python server.py
No TikTok information found	Username không tồn tại	Kiểm tra lại username
Failed to initialize browser	Chrome chưa cài đặt	Cài Google Chrome
Timeout error	Mạng chậm/Server tải	Thử lại sau vài phút
HTTP Error 429	Rate limiting	Đợi vài phút trước khi thử lại
Debug Mode
Server tự động tạo các file debug khi gặp lỗi:

debug_screenshot.png: Ảnh chụp màn hình trang web

debug_page.html: Mã nguồn HTML đầy đủ

selenium_result_*.html: Kết quả từ Selenium

Logging
Kiểm tra terminal để xem log chi tiết:

bash
# Server logs
Checking TikTok account: tiktok
Trying Selenium method...
Navigating to: https://omar-thing.site/

# Client logs
🔍 Checking account: @tiktok
⏳ Please wait... (This may take 10-20 seconds)
🤝 Đóng góp
Đóng góp luôn được chào đón! Hãy:

Fork repository

Tạo branch mới (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add some AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Mở Pull Request

Quy tắc đóng góp
Tuân thủ PEP 8 style guide

Viết comment cho code phức tạp

Cập nhật documentation khi cần

Test kỹ trước khi submit

📄 Giấy phép
Distributed under the MIT License. See LICENSE file for more information.

⚠️ Disclaimer
Dự án này chỉ dành cho mục đích giáo dục và nghiên cứu.

Không sử dụng để spam hoặc vi phạm điều khoản dịch vụ

Tôn trọng quyền riêng tư của người dùng

Dữ liệu được lấy từ nguồn công khai

Không chịu trách nhiệm cho việc sử dụng sai mục đích

🌟 Sao repository này
Nếu bạn thấy dự án này hữu ích, hãy cho nó một ngôi sao ⭐ trên GitHub!

📞 Liên hệ & Hỗ trợ
Báo lỗi: Mở issue

Câu hỏi: Kiểm tra FAQ hoặc mở discussion

Đề xuất tính năng: Mở issue với label "enhancement"

<div align="center">
Made with ❤️ bằng Python
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white

</div>
🚀 Quick Start
bash
# Clone và chạy nhanh
git clone https://github.com/yourusername/tiktok-analyzer.git
cd tiktok-analyzer
python server.py &  # Chạy server ở background
python client.py    # Chạy client
Chúc bạn sử dụng vui vẻ! 🎉

