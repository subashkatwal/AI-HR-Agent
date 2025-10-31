from pydantic import BaseModel, Field
from typing import List , Optional 

class Education(BaseModel):
    institution : Optional[str]= None
    start_date: Optional[str] = None 
    end_date: Optional[str] = None
    degree: Optional[str] = None

class Project(BaseModel):
    name: Optional[str]
    description: Optional[str]
    duration: Optional[str]

class WorkExperience(BaseModel):
    company : Optional[str]= None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    role: Optional[str] = None

class Resume(BaseModel):
    name: Optional[str] = None 
    end_date: Optional[str] = None 
    contact_number: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    educations: List[Education] = Field(default_factory=list)
    work_experiences: List[WorkExperience] = Field(default_factory=list)
    YoE: Optional[str] = None

    @classmethod
    def model_json_schema(cls):
        return super().model_json_schema()
    

