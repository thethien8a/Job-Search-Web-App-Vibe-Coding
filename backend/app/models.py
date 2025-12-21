"""
SQLAlchemy Models
Maps to the api_serving_staging_jobs view in PostgreSQL
"""
from sqlalchemy import Column, String
from app.database import Base


class StagingJob(Base):
    """
    Model for the api_serving_staging_jobs view.
    This is a read-only view for serving job data via API.
    """
    __tablename__ = "api_serving_staging_jobs"
    
    # job_url is used as primary key since views don't have auto-increment id
    job_url = Column(String(1000), primary_key=True)
    job_title = Column(String(500), nullable=False, index=True)
    company_name = Column(String(500), nullable=False, index=True)
    salary = Column(String(500), nullable=True)
    location = Column(String(500), nullable=True, index=True)
    experience_level = Column(String(500), nullable=True)
    job_deadline = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<Job(title={self.job_title}, company={self.company_name})>"
