from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from typing import Annotated
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from models import Developer
import models

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI running fine!"}


app=FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]    

class DeveloperBase(BaseModel):
    name: str
    email: str
    skills: str
    experience_years: int
    phone_number: int

@app.post("/developers/", status_code=status.HTTP_201_CREATED)
async def register_developer(developer: DeveloperBase, db: db_dependency):
    db_developer = Developer(**developer.dict())
    db.add(db_developer)
    db.commit()
    db.refresh(db_developer)
    return {"message": f"Developer {developer.name} registered successfully!", "developer_id": db_developer.id}

@app.get("/developers/{developer_id}", status_code=status.HTTP_200_OK)
async def get_developer(developer_id: int, db: db_dependency):
    developer = db.query(Developer).filter(Developer.id == developer_id).first()
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



