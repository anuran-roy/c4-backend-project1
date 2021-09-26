from pydantic import BaseModel # Base class for request bodies
from typing import Optional

class Blog(BaseModel):
    title: str
    description: str
    published: Optional[bool]

class ShowBlog(BaseModel):
    title: str
    description: str
    published: Optional[bool]
class ShowList(BaseModel):
    title: str

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserProfile(BaseModel):
    name: str
    username: str
    email: str

    class Config():
        orm_mode = True