-- ============================================================
-- INDEX SCRIPT CHO BẢNG silver_jobs
-- Job Search Web Application
-- ============================================================

-- Bước 0: Enable extension pg_trgm (CHẠY TRƯỚC)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================
-- 1. INDEX CHO FILTER THỜI GIAN (QUAN TRỌNG NHẤT)
-- Mục đích: Lọc 30 ngày gần nhất + sắp xếp tin mới nhất
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_silver_jobs_scraped_at 
ON public_app_layer.silver_jobs (scraped_at DESC);

-- ============================================================
-- 2. INDEX CHO BỘ LỌC DROPDOWN (location, job_type, work_arrangement)
-- Mục đích: Filter ILIKE + SELECT DISTINCT cho dropdown
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_silver_jobs_location 
ON public_app_layer.silver_jobs (location);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_job_type 
ON public_app_layer.silver_jobs (job_type);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_work_arrangement 
ON public_app_layer.silver_jobs (work_arrangement);

-- ============================================================
-- 3. INDEX CHO TÌM KIẾM FUZZY (pg_trgm) - TYPO TOLERANCE
-- Mục đích: 
--   - Tăng tốc ILIKE '%keyword%'
--   - Hỗ trợ similarity() cho fuzzy search
--   - Ví dụ: "data analystt" → "data analyst"
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_silver_jobs_trgm_title 
ON public_app_layer.silver_jobs USING GIN (job_title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_silver_jobs_trgm_position 
ON public_app_layer.silver_jobs USING GIN (job_position gin_trgm_ops);

-- ============================================================
-- 4. INDEX CHO FULL-TEXT SEARCH (English stemming)
-- Mục đích:
--   - Tìm kiếm ngữ nghĩa tiếng Anh
--   - Ví dụ: "analysts" → "analyst", "running" → "run"
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_silver_jobs_fts_title 
ON public_app_layer.silver_jobs 
USING GIN (to_tsvector('english', COALESCE(job_title, '')));

CREATE INDEX IF NOT EXISTS idx_silver_jobs_fts_position 
ON public_app_layer.silver_jobs 
USING GIN (to_tsvector('english', COALESCE(job_position, '')));

-- ============================================================
-- KIỂM TRA INDEX ĐÃ TẠO
-- ============================================================
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public_app_layer' 
  AND tablename = 'silver_jobs'
ORDER BY indexname;