from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    email: str
    password: str
    role: str  
    profile: Optional[dict] = {}

class Job(BaseModel):
    title: str
    description: str
    skills: List[str]
    salary: int
    location: str
    # employer_id: Optional[str]

# class Application(BaseModel):
#     job_id: str
#     job_title: str
#     status: str
#     applied_on: str
