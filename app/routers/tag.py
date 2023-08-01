from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/tags",
    tags=['Tags']
)

@router.get("/", response_model=List[schemas.TagOut])
def get_tags(limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(get_db)):
    db_tags = db.query(models.Tag).filter(models.Tag.tag.contains(search)).limit(limit).offset(skip).all()
    return db_tags

@router.get("/{recipe_id}", response_model=List[schemas.TagOut])
def get_tag(
    recipe_id: int,
    db: Session = Depends(get_db)
    ):
    db_tag = db.query(models.Tag).filter(models.Tag.recipe_id == recipe_id).all()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.post("/{recipe_id}/tags", response_model=schemas.TagOut)
def create_tags(
    recipe_id: int,
    tags: List[schemas.TagIn],
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    for tag in tags:
            db_tag = models.Tag(
                recipe_id=recipe_id,
                tag=tag.tag,
                tag_number=tag.tag_number
            )
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)

    return db_tag

@router.put("/{tag_id}", response_model=schemas.TagOut)
def update_tag(
    tag_id: int,
    tag: schemas.TagIn,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_tag.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db_tag.tag = tag.tag
    db_tag.tag_number = tag.tag_number

    db.commit()
    db.refresh(db_tag)

    return db_tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_tag.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(db_tag)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
