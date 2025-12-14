from typing import Annotated, TypedDict, Dict, Any
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str = Field(description="The title of the blog post")
    content:str = Field(description="The main content of the blog post")

class BlogState(TypedDict):
    """ 
    Represent the structure of the blog state used in graph
    
    """
    topic:str
    blog:Blog
    current_language:str 
    translated_content: str 
    final_post: Dict[str, Any] 