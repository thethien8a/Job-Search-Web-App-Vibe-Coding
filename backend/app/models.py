"""
SQLAlchemy Models
Maps to the api_serving_staging_jobs view in PostgreSQL
"""
from sqlalchemy import Column, String, TIMESTAMP
from app.database import Base


class SilverJob(Base):
    """
    Model for the public_app_layer.silver_jobs table.
    """
    __tablename__ = "silver_jobs"
    __table_args__ = {"schema": "public_app_layer"}
    
    # assuming we need a primary key, keeping job_url if available, or we might need an id.
    # User didn't specify PK, but logic requires one. usage of job_url in codebase suggests it's the id.
    job_url = Column(String, primary_key=True) 
    job_title = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True, index=True)
    job_type = Column(String, nullable=True)
    job_position = Column(String, nullable=True, index=True)
    job_deadline = Column(String, nullable=True)
    work_arrangement = Column(String, nullable=True)
    scraped_at = Column(TIMESTAMP, nullable=True)
    
    def __repr__(self):
        return f"<Job(title={self.job_title}, company={self.company_name})>"
