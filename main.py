from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import Optional, List # For optional parameters
from schemas import Blog, User, ShowBlog, ShowList, UserProfile
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
        print("Accessing DB...")
        yield db
    finally:
        db.close()

#################################### Paths ####################################

@app.get('/')  # Sends GET request to path '/'
async def helloworld():  # Path operation function
    return {"data": {"Hello": "world"}}

@app.get("/about/")
async def about():
    return {"data": 
        {
            "name": "Anuran",
            "age": 19,
            "batch": "2020-24"
        }
    }

@app.get('/blog/', tags=['blog'])
async def index(limit: int=10, published: bool = True, sort: Optional[str] = None, db: Session = Depends(get_db)):
    lst = db.query(models.Blog).all()
    if sort == 'ascending':
        lst.sort(key = lambda x: x.id)
    elif sort == 'descending':
        lst.sort(reverse=True, key = lambda x: x.id)
    if published:
        return {"data": {"blog list": lst[:limit], "count": min(len(lst),limit)}}
    else:
        return {"data": {"blog_id": "all unpublished stuff"}}

@app.get('/blog/all', response_model = List[ShowList], tags=['blog'])
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=['blog'])
async def get(id: int,  response: Response, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()
    # print(f"\n\n{entry}\n\n")
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found")
    return entry

@app.get('/blog/{id}/{action}', response_model=ShowBlog, tags=['blog'])
async def get(id: int, action: str):
    if action == "comments":
        return {
            "data": {
                "blog_id": id, 
                "comments": [
                    "comment 1",
                    "comment 2",
                    "comment 3",
                    ]
                }
            }

@app.post('/blog/', status_code = status.HTTP_201_CREATED, tags=['blog'])
async def createBlog(blog: Blog, response: Response, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    response.status_code = status.HTTP_201_CREATED
    # return new_blog
    return {"details": "OK"}

@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED, response_model=ShowBlog, tags=['blog'])
async def editPost(id: int, blog: Blog, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not entry:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Not found")
    
    db.query(models.Blog).filter(models.Blog.id == id).update({"title": blog.title, "description": blog.description})
    db.commit()
    return {"response": "OK"}

@app.delete('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
async def deleteEntry(id: int, response: Response, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not entry:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Not found")

    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {"details": "OK"}

#################################### Users ####################################

@app.post('/user', tags=['users'])
def createUser(request: User, db: Session = Depends(get_db)):
    hashedPassword = Hash().bcrypt(request.password)
    new_user = models.User(name=request.name, username=request.username, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user/{username}', response_model = UserProfile, tags=['users'])
def getByUsername(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
 
    return user

#################################### Uvicorn deployment ####################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)