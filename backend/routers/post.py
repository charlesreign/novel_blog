from enum import Enum
import random
import shutil
import string
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, status, Response, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from database.database import get_db
from routers.schemas import PostBase
from database import db_post


router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/post")
def create(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create_article(db, request)


@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.delete("/delete")
def delette_post(id: int, db: Session = Depends(get_db)):
    return db_post.delete(id, db)


@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = "".join(random.choice(letter) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit('.', 1))
    path = f"images/{filename}"

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}