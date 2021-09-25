from pydantic import BaseModel # Base class for request bodies
from typing import Optional

class Blog(BaseModel):
    title: str
    description: str
    published: Optional[bool]