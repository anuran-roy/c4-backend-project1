from fastapi import FastAPI, Depends, Response, status, HTTPException
from typing import Optional # For optional parameters
from schemas import Blog
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()

    try:
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

@app.get('/blog/')
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

@app.get('/blog/all')
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
async def get(id: int,  response: Response, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()
    # print(f"\n\n{entry}\n\n")
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found")
    return entry

@app.get('/blog/{id}/{action}')
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

@app.post('/blog/', status_code = status.HTTP_201_CREATED)
async def createBlog(blog: Blog, response: Response, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    response.status_code = status.HTTP_201_CREATED
    # return new_blog
    return {"details": "OK"}

@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED)
async def editPost(id: int, blog: Blog, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not entry:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Not found")
    
    db.query(models.Blog).filter(models.Blog.id == id).update({"title": blog.title, "description": blog.description})
    db.commit()
    return {"response": "OK"}

@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
async def deleteEntry(id: int, response: Response, db: Session = Depends(get_db)):
    entry = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not entry:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Not found")

    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {"details": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)