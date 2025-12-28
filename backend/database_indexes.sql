-- Chạy các lệnh này trong SQL Editor của Supabase để tối ưu hóa tốc độ truy vấn

-- 1. Index cho cột thời gian (QUAN TRỌNG NHẤT)
-- Lý do: API luôn mặc định lọc 30 ngày gần nhất và sắp xếp tin mới nhất.
-- Index này giúp query chạy ngay lập tức thay vì quét toàn bộ bảng.
CREATE INDEX IF NOT EXISTS idx_silver_jobs_scraped_at 
ON public_app_layer.silver_jobs (scraped_at DESC);

-- 2. Index cho các bộ lọc Dropdown (Địa điểm, Loại hình, Hình thức làm việc)
-- Lý do: Giúp hiển thị danh sách trong bộ lọc nhanh hơn và lọc kết quả nhanh hơn.
CREATE INDEX IF NOT EXISTS idx_silver_jobs_location 
ON public_app_layer.silver_jobs (location);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_job_type 
ON public_app_layer.silver_jobs (job_type);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_work_arr 
ON public_app_layer.silver_jobs (work_arrangement);

-- 3. Index cho Tìm kiếm thông minh (Full Text Search)
-- Lý do: Hỗ trợ tìm kiếm từ khóa tiếng Anh, số ít/số nhiều (Data Analysts -> Analyst).
-- Sử dụng GIN Index, loại index chuyên dụng cho tìm kiếm văn bản.
CREATE INDEX IF NOT EXISTS idx_silver_jobs_fts_title 
ON public_app_layer.silver_jobs 
USING GIN (to_tsvector('english', coalesce(job_title, '')));

CREATE INDEX IF NOT EXISTS idx_silver_jobs_fts_position 
ON public_app_layer.silver_jobs 
USING GIN (to_tsvector('english', coalesce(job_position, '')));

-- 4. FUZZY SEARCH với pg_trgm (Tìm kiếm có khả năng chịu lỗi đánh máy)
-- Lý do: Khi user gõ nhầm "data analystt" thay vì "data analyst", 
-- hệ thống vẫn trả về kết quả phù hợp nhờ so sánh trigram (3-ký tự).
-- Extension pg_trgm giúp:
--   ✓ Fuzzy search (tìm kiếm mờ)
--   ✓ Typo tolerance (chịu lỗi đánh máy)
--   ✓ Tìm kiếm chuỗi con nhanh với ILIKE

-- B1: Enable extension pg_trgm (CHẠY LỆNH NÀY TRƯỚC)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- B2: Tạo GIN Index cho fuzzy search trên job_title và job_position
-- GIN index với gin_trgm_ops giúp tăng tốc độ similarity() và ILIKE
CREATE INDEX IF NOT EXISTS idx_silver_jobs_trgm_title 
ON public_app_layer.silver_jobs USING GIN (job_title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_trgm_position 
ON public_app_layer.silver_jobs USING GIN (job_position gin_trgm_ops);

-- B3: (Tùy chọn) Điều chỉnh ngưỡng similarity mặc định
-- Mặc định PostgreSQL sử dụng 0.3 (30%). Có thể thay đổi tùy nhu cầu:
-- SELECT set_limit(0.2); -- Giảm xuống 20% để linh hoạt hơn
