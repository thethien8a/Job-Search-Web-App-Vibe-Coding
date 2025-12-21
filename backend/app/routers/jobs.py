"""
Jobs API Router
Handles all job-related endpoints with search and pagination
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app.models import StagingJob
from app.schemas import JobSummary, JobDetail, PaginatedResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=PaginatedResponse)
async def search_jobs(
    keyword: Optional[str] = Query(None, max_length=100, description="Search in job title, company"),
    location: Optional[str] = Query(None, max_length=100, description="Filter by location"),
    company: Optional[str] = Query(None, max_length=100, description="Filter by company name"),
    experience_level: Optional[str] = Query(None, max_length=50, description="Filter by experience level"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Search and list jobs with filtering and pagination.
    
    - **keyword**: Search in job title and company name
    - **location**: Filter by job location (partial match)
    - **company**: Filter by company name (partial match)
    - **experience_level**: Filter by experience level (partial match)
    - **page**: Page number for pagination
    - **page_size**: Number of items per page (max 100)
    """
    # Base query
    query = db.query(StagingJob)
    
    # Apply filters using parameterized queries (SQL injection safe)
    if keyword:
        search_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                StagingJob.job_title.ilike(search_pattern),
                StagingJob.company_name.ilike(search_pattern)
            )
        )
    
    if location:
        query = query.filter(StagingJob.location.ilike(f"%{location}%"))
    
    if company:
        query = query.filter(StagingJob.company_name.ilike(f"%{company}%"))
    
    if experience_level:
        query = query.filter(StagingJob.experience_level.ilike(f"%{experience_level}%"))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    offset = (page - 1) * page_size
    
    # Get paginated results, ordered by job_title
    jobs = query.order_by(StagingJob.job_title).offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=[JobSummary.model_validate(job) for job in jobs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/locations", response_model=list[str])
async def get_job_locations(db: Session = Depends(get_db)):
    """Get list of all available job locations for filtering."""
    locations = db.query(StagingJob.location).distinct().limit(100).all()
    return [loc[0] for loc in locations if loc[0]]


@router.get("/experience-levels", response_model=list[str])
async def get_experience_levels(db: Session = Depends(get_db)):
    """Get list of all available experience levels for filtering."""
    levels = db.query(StagingJob.experience_level).distinct().limit(50).all()
    return [level[0] for level in levels if level[0]]


@router.get("/stats")
async def get_job_stats(db: Session = Depends(get_db)):
    """Get general statistics about available jobs."""
    total_jobs = db.query(func.count(StagingJob.job_url)).scalar()
    total_companies = db.query(func.count(func.distinct(StagingJob.company_name))).scalar()
    
    # Jobs by location (top 10)
    jobs_by_location = db.query(
        StagingJob.location,
        func.count(StagingJob.job_url)
    ).group_by(StagingJob.location).order_by(func.count(StagingJob.job_url).desc()).limit(10).all()
    
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
    job = db.query(StagingJob).filter(StagingJob.job_url == job_url).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobDetail.model_validate(job)
