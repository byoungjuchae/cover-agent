from typing_extensions import Annotated, TypedDict, Optional
from pydantic import BaseModel
from langgraph.graph.message import add_messages, AnyMessage

class SwarmState(TypedDict):
    id: str
    messages: Annotated[list[AnyMessage], add_messages]
    plan : Optional[str]
    jd_check : Optional[str]
    response: Optional[str]
    result: Optional[str]

class SuperState(TypedDict):
    
    id: str
    messages: Annotated[list[AnyMessage], add_messages]
    
class WriteState(TypedDict):
    
    text : str
    input_pdf : str
    input_JD : str
    response_pdf : str
    response_JD : str
    result : str
    score : str
    
    
class JobSearchConfig(BaseModel):
    job: str
    start_day: str
    start_month: str
    start_year: str
    end_day: str
    end_month: str
    end_year: str
    
class OuterModel(BaseModel):
    request: str
    name : str
    
class JobDescriptionRequest(BaseModel):
 
    description: str