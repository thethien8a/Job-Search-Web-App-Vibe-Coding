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
    
    # Apply filters using parameterized queries (SQL injection safe)
    if keyword:
        # Get expanded search terms (Bilingual support)
        search_patterns = get_expanded_search_terms(keyword)
        
    if keyword:
        # 1. Existing Logic: Expanded search terms (Synonyms + Partial Match)
        search_patterns = get_expanded_search_terms(keyword)
        
        match_conditions = []
        
        # Condition A: ILIKE (Partial match & Synonyms - Good for Vietnamese & exact substrings)
        for pattern in search_patterns:
            match_conditions.append(SilverJob.job_title.ilike(pattern))
            match_conditions.append(SilverJob.job_position.ilike(pattern))
            
        # Condition B: Full Text Search
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
        
        # Combine all conditions with OR
        query = query.filter(or_(*match_conditions))
    
    if location:
        query = query.filter(SilverJob.location.ilike(f"%{location}%"))
    
    if job_type:
        query = query.filter(SilverJob.job_type.ilike(f"%{job_type}%"))
    
    if work_arrangement:
        query = query.filter(SilverJob.work_arrangement.ilike(f"%{work_arrangement}%"))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    offset = (page - 1) * page_size
    
    # Get paginated results, ordered by scraped_at desc (newest first), then job_title
    jobs = query.order_by(SilverJob.scraped_at.desc(), SilverJob.job_title).offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=[JobSummary.model_validate(job) for job in jobs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


from app.utils import cache_response, dropdown_cache

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
@cache_response(dropdown_cache)
async def get_job_stats(db: Session = Depends(get_db)):
    """Get general statistics about available jobs."""
    total_jobs = db.query(func.count(SilverJob.job_url)).scalar()
    total_companies = db.query(func.count(func.distinct(SilverJob.company_name))).scalar()
    
    # Jobs by location (top 10)
    jobs_by_location = db.query(
        SilverJob.location,
        func.count(SilverJob.job_url)
    ).group_by(SilverJob.location).order_by(func.count(SilverJob.job_url).desc()).limit(10).all()
    
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
