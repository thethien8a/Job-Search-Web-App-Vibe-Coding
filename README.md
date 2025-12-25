# 🔎 Job Search Web App - Vibe Coding

Chào mừng bạn đến với **Job Search Web App**, một công cụ tìm kiếm việc làm hiện đại, thông minh và có hiệu năng cao. Dự án này được xây dựng với mục tiêu cung cấp trải nghiệm tra cứu tin tuyển dụng tối ưu nhất.

![Project Banner](https://via.placeholder.com/1200x400?text=Job+Search+Web+App)

## 🚀 Tính Năng Nổi Bật

### 1. 🧠 Tìm Kiếm Thông Minh (Hybrid Search)
Hệ thống kết hợp giữa tìm kiếm chính xác và xử lý ngôn ngữ tự nhiên:
- **Song ngữ (Anh - Việt):** Tìm "Intern" tự động ra kết quả "Thực tập".
- **Fuzzy Matching:** Tìm "Data Analysts" (số nhiều) vẫn ra "Data Analyst" (số ít).
- **Full Text Search:** Tối ưu hóa truy vấn văn bản, bỏ qua lỗi ngữ pháp nhỏ.

### 2. ⚡ Hiệu Năng Cao
- **Smart Caching:** Lưu bộ đệm các dữ liệu ít thay đổi (Địa điểm, Ngành nghề) giúp tải trang tức thì.
- **Tối ưu Database:** Sử dụng Index (GIN, B-Tree) cho tốc độ truy vấn "xé gió".
- **Dữ liệu Tươi:** Tự động lọc các tin rác, chỉ hiển thị tin tuyển dụng trong vòng 30 ngày gần nhất.

### 3. @ Giao Diện Hiện Đại
- Thiết kế tối giản, tập trung vào nội dung.
- Bộ lọc chuyên sâu: Ngành nghề, Địa điểm, Hình thức làm việc (Remote/Onsite).

---

## 🛠️ Công Nghệ Sử Dụng

**Frontend:**
- **React (Vite):** Tốc độ build siêu nhanh.
- **TailwindCSS:** Giao diện đẹp, responsive.
- **TanStack Query:** Quản lý state server hiệu quả.
- **Nginx:** Web Server & Reverse Proxy mạnh mẽ.

**Backend:**
- **FastAPI:** Python framework hiệu năng cao.
- **SQLAlchemy:** ORM tương tác database an toàn.
- **Pydantic:** Validate dữ liệu chặt chẽ.
- **PostgreSQL:** Cơ sở dữ liệu quan hệ mạnh mẽ.

---

## 🔧 Hướng Dẫn Cài Đặt & Chạy Dự Án

### Cách 1: Chạy với Docker (Khuyên dùng)
Đây là cách nhanh nhất để trải nghiệm trọn bộ hệ thống (Frontend + Backend + Database local).

1. **Yêu cầu:** Máy đã cài Docker & Docker Compose.
2. **Chạy lệnh:**
   ```bash
   docker-compose up -d --build
   ```
3. **Truy cập:**
   - Web App: `http://localhost`
   - API Docs: `http://localhost:8000/api/docs`

> **Lưu ý:** Lần chạy đầu tiên, Database sẽ tự động khởi tạo dữ liệu mẫu (nhờ file `init_db.sql`).

### Cách 2: Chạy với Database Cloud (Supabase)
Nếu bạn đã có database trên Supabase và muốn backend kết nối tới đó.

1. Tạo file `.env` tại thư mục gốc:
   ```env
   # Database Config
   POSTGRES_HOST=db.xxx.supabase.co
   POSTGRES_PORT=5432
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password

   # App Config
   API_DEBUG=false
   CORS_ORIGINS=http://localhost,http://localhost:3000
   ```
2. Chạy Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
   *Hệ thống sẽ tự nhận diện host lạ và bật chế độ SSL an toàn.*

---

## 📂 Cấu Trúc Dự Án

```
JobSearchWeb/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── routers/        # API Endpoints
│   │   ├── models.py       # DB Models
│   │   └── schemas.py      # Pydantic Schemas
│   ├── init_db.sql         # Script khởi tạo DB Local
│   └── Dockerfile
├── frontend/               # React Application
│   ├── src/
│   ├── nginx.conf          # Cấu hình Web Server Production
│   └── Dockerfile
├── docker-compose.yml      # Orchestration
└── README.md
```

## 🤝 Đóng Góp

Mọi ý kiến đóng góp đều được hoan nghênh. Hãy tạo Pull Request hoặc Issue nếu bạn tìm thấy lỗi nhé!

---
*Built with ❤️ by Thế Thiện*
