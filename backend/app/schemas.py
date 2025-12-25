"""
Pydantic Schemas for Request/Response Validation
Ensures data integrity and provides automatic API documentation
"""
from typing import Optional, Union
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class JobBase(BaseModel):
    """Base schema for Job data."""
    job_title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    job_type: Optional[str] = Field(None, description="Type of job (e.g. Full-time)")
    job_position: Optional[str] = Field(None, description="Job position (e.g. Intern, Senior)")
    job_deadline: Optional[Union[date, str]] = Field(None, description="Application deadline")
    work_arrangement: Optional[str] = Field(None, description="Work arrangement (e.g. Remote, Onsite)")


class JobSummary(JobBase):
    """Schema for job listing (summary view)."""
    job_url: str = Field(..., description="Original job URL")
    
    model_config = ConfigDict(from_attributes=True)


class JobDetail(JobSummary):
    """Schema for full job details (same as summary since view has limited fields)."""
    
    model_config = ConfigDict(from_attributes=True)


class JobSearchParams(BaseModel):
    """Schema for search query parameters."""
    keyword: Optional[str] = Field(None, max_length=100, description="Search keyword")
    location: Optional[str] = Field(None, max_length=100, description="Filter by location")
    job_type: Optional[str] = Field(None, max_length=50, description="Filter by job type")
    work_arrangement: Optional[str] = Field(None, max_length=50, description="Filter by work arrangement")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel):
    """Schema for paginated API responses."""
    items: list[JobSummary]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = "healthy"
    database: str = "connected"
    version: str = "1.0.0"
