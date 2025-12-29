"""
Jobs API Router
Handles all job-related endpoints with search and pagination
"""
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app.models import SilverJob
from app.schemas import JobSummary, JobDetail, PaginatedResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# Bilingual Synonym Groups for Smart Search
SYNONYM_GROUPS = [
    {"intern", "thực tập", "trainee", "intership"},
    {"fresher", "mới tốt nghiệp", "graduate", "junior", "nhân viên", "chuyên viên"},
    {"senior", "cao cấp", "chuyên gia", "expert", "trưởng nhóm", "team lead", "lead"},
    {"manager", "quản lý", "trưởng phòng", "head"},
    {"director", "giám đốc"},
    {"part-time", "bán thời gian"},
    {"full-time", "toàn thời gian"},
    {"remote", "từ xa", "online", "tại nhà"},
]

def get_expanded_search_terms(keyword: str) -> list[str]:
    """
    Expand keyword to include synonyms if a match is found.
    Returns a list of search patterns (e.g. ['%intern%', '%thực tập%']).
    """
    keyword_lower = keyword.lower().strip()
    search_terms = {keyword_lower}
    
    # Check if keyword matches any synonym group
    for group in SYNONYM_GROUPS:
        # Check if any word in the group is part of the keyword or vice versa
        # Using simple containment check
        if any(term in keyword_lower for term in group) or any(keyword_lower in term for term in group):
            search_terms.update(group)
            
    return [f"%{term}%" for term in search_terms]


@router.get("", response_model=PaginatedResponse)
async def search_jobs(
    keyword: Optional[str] = Query(None, max_length=100, description="Search in job title, job position"),
    location: Optional[str] = Query(None, max_length=100, description="Filter by location"),
    job_type: Optional[str] = Query(None, max_length=50, description="Filter by job type"),
    work_arrangement: Optional[str] = Query(None, max_length=50, description="Filter by work arrangement"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Search and list jobs with filtering and pagination.
    
    - **keyword**: Search in job title and job position (Smart Search with Bilingual support)
    - **location**: Filter by job location
    - **job_type**: Filter by job type (e.g. Full-time)
    - **work_arrangement**: Filter by work arrangement (e.g. Remote)
    - **page**: Page number for pagination
    - **page_size**: Number of items per page (max 100)
    """
    # Base query
    cutoff_date = datetime.now() - timedelta(days=30)
    query = db.query(SilverJob).filter(SilverJob.scraped_at >= cutoff_date)
    
    # Apply keyword search with Smart Search (Synonyms, Full-text, Fuzzy)
    if keyword:
        # 1. Existing Logic: Expanded search terms (Synonyms + Partial Match)
        search_patterns = get_expanded_search_terms(keyword)
        
        match_conditions = []
        
        # Condition A: ILIKE (Partial match & Synonyms - Good for Vietnamese & exact substrings)
        for pattern in search_patterns:
            match_conditions.append(SilverJob.job_title.ilike(pattern))
            match_conditions.append(SilverJob.job_position.ilike(pattern))
            
        # Condition B: Full Text Search (for English stemming: analyst -> analysts)
        # Using explicit @@ operator instead of .match() to avoid SQL generation errors with func.plainto_tsquery
        match_conditions.append(
            func.to_tsvector('english', func.coalesce(SilverJob.job_title, '')).op("@@")(
                func.plainto_tsquery('english', keyword)
            )
        )
        match_conditions.append(
            func.to_tsvector('english', func.coalesce(SilverJob.job_position, '')).op("@@")(
                func.plainto_tsquery('english', keyword)
            )
        )
        
        # Condition C: FUZZY SEARCH using pg_trgm (Typo tolerance)
        # This allows "data analystt" to match "data analyst"
        # Using similarity threshold of 0.25 (25%) - optimized for job search
        # Lower threshold = more forgiving for typos
        similarity_threshold = 0.25
        
        # Fuzzy match on job_title
        match_conditions.append(
            func.similarity(SilverJob.job_title, keyword) >= similarity_threshold
        )
        
        # Fuzzy match on job_position
        match_conditions.append(
            func.similarity(SilverJob.job_position, keyword) >= similarity_threshold
        )
        
        # Combine all conditions with OR
        query = query.filter(or_(*match_conditions))
    
    if location:
        query = query.filter(SilverJob.location.ilike(f"%{location}%"))
    
    if job_type:
        query = query.filter(SilverJob.job_type.ilike(f"%{job_type}%"))
    
    if work_arrangement:
        query = query.filter(SilverJob.work_arrangement.ilike(f"%{work_arrangement}%"))
    
    # FIX v3: Fetch ALL matching IDs, Sort & Paginate in Python
    # This bypasses all PostgreSQL optimizer issues with mixing LIMIT/OFFSET and complex GIN index searches.
    # Why? Because if PG picks a bad plan, "ORDER BY ... LIMIT 20" might return 20 random rows 
    # instead of the top 20 sorted rows.
    
    # Step 1: Get ALL matching job_urls and scraped_at (limit 2000 to be safe)
    # clear existing order just in case
    query = query.order_by(None)
    
    all_matches = query.with_entities(
        SilverJob.job_url, 
        SilverJob.scraped_at,
        SilverJob.job_deadline, # fetch deadline for sorting
        SilverJob.job_title # fetch title for fallback sort
    ).limit(2000).all()
    
    # Step 2: Sort in Python (Reliable)
    # Sort by scraped_at DATE (so jobs scraped on the same day are grouped), 
    # then job_deadline DESC (furthest deadline first), then title.
    # Convert all to string to avoid TypeError between date and str types
    all_matches.sort(
        key=lambda x: (
            str(x.scraped_at.date()) if x.scraped_at else "1970-01-01", 
            str(x.job_deadline) if x.job_deadline else "", 
            str(x.job_title) or ""
        ), 
        reverse=True
    )
    
    # Get total from the fetched list (or actual count if > 2000, roughly)
    total_fetched = len(all_matches)
    if total_fetched < 2000:
        total = total_fetched
    else:
        # If we hit the limit, fallback to query.count() for accurate total
        # Note: Pagination beyond 2000 items might be inconsistent but acceptable for search results
        total = query.count()
        
    # Step 3: Paginate in Python
    # Calculate slice indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Slice the sorted list
    page_items = all_matches[start_idx:end_idx]
    
    sorted_job_urls = [item.job_url for item in page_items]
    
    # Step 4: Fetch full objects for the current page
    if sorted_job_urls:
        jobs_dict = {
            job.job_url: job 
            for job in db.query(SilverJob).filter(
                SilverJob.job_url.in_(sorted_job_urls)
            ).all()
        }
        # Preserve order
        jobs = [jobs_dict[url] for url in sorted_job_urls if url in jobs_dict]
    else:
        jobs = []

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    return PaginatedResponse(
        items=[JobSummary.model_validate(job) for job in jobs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


from app.utils import cache_response, dropdown_cache, search_cache

@router.get("/locations", response_model=list[str])
@cache_response(dropdown_cache)
async def get_job_locations(db: Session = Depends(get_db)):
    """Get list of all available job locations for filtering."""
    locations = db.query(SilverJob.location).distinct().limit(100).all()
    return [loc[0] for loc in locations if loc[0]]


@router.get("/job-types", response_model=list[str])
@cache_response(dropdown_cache)
async def get_job_types(db: Session = Depends(get_db)):
    """Get list of all available job types."""
    types = db.query(SilverJob.job_type).distinct().limit(50).all()
    return [t[0] for t in types if t[0]]


@router.get("/work-arrangements", response_model=list[str])
@cache_response(dropdown_cache)
async def get_work_arrangements(db: Session = Depends(get_db)):
    """Get list of all available work arrangements."""
    arrangements = db.query(SilverJob.work_arrangement).distinct().limit(50).all()
    return [arr[0] for arr in arrangements if arr[0]]


@router.get("/stats")
@cache_response(search_cache)
async def get_job_stats(db: Session = Depends(get_db)):
    """Get general statistics about available jobs (scraped in last 30 days)."""
    cutoff_date = datetime.now() - timedelta(days=30)
    
    total_jobs = db.query(func.count(SilverJob.job_url))\
        .filter(SilverJob.scraped_at >= cutoff_date).scalar()
        
    total_companies = db.query(func.count(func.distinct(SilverJob.company_name)))\
        .filter(SilverJob.scraped_at >= cutoff_date).scalar()
    
    # Jobs by location (top 10)
    jobs_by_location = db.query(
        SilverJob.location,
        func.count(SilverJob.job_url)
    ).filter(SilverJob.scraped_at >= cutoff_date)\
    .group_by(SilverJob.location)\
    .order_by(func.count(SilverJob.job_url).desc())\
    .limit(10).all()
    
    return {
        "total_jobs": total_jobs,
        "total_companies": total_companies,
        "jobs_by_location": {loc: count for loc, count in jobs_by_location if loc}
    }


@router.get("/{job_url:path}", response_model=JobDetail)
async def get_job_detail(job_url: str, db: Session = Depends(get_db)):
    """
    Get full details of a specific job by URL.
    
    - **job_url**: The URL of the job posting
    """
    job = db.query(SilverJob).filter(SilverJob.job_url == job_url).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobDetail.model_validate(job)
