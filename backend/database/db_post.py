from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from database.models import DbPost
from routers.schemas import PostBase
from datetime import datetime


def create_article(db: Session, request: PostBase):
    new_article = DbPost(
        image_url=request.image_url,
        title=request.title,
        content=request.content,
        creator=request.creator,
        timestamp=datetime.now(),
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_all(db: Session):
    return db.query(DbPost).all()


def delete(id: int, db: Session):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"article with id={id} not found",
        )
    db.delete(post)
    db.commit()
    return {"status": "OK", "status_code": 200}
