from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/steps",
    tags=['Step']
)

@router.get("/", response_model=List[schemas.StepOut])
def get_steps(    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(get_db)):
    db_steps = db.query(models.Step).filter(models.Step.step.contains(search)).limit(limit).offset(skip).all()
    return db_steps

@router.get("/{recipe_id}", response_model=List[schemas.StepOut])
def get_step(
    recipe_id: int,
    db: Session = Depends(get_db)
    ):
    db_steps = db.query(models.Step).filter(models.Step.recipe_id == recipe_id).all()
    if db_steps is None:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_steps

@router.post("/{recipe_id}/steps", response_model=schemas.StepOut)
def create_steps(
    recipe_id: int,
    steps: List[schemas.StepIn],
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    for step in steps:
        db_step = models.Step(
            recipe_id=recipe_id,
            step=step.step,
            step_number=step.step_number
        )
        db.add(db_step)
        db.commit()
        db.refresh(db_step)

    return db_step

@router.put("/{step_id}", response_model=schemas.StepOut)
def update_step(
    step_id: int,
    step: schemas.StepIn,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_step = db.query(models.Step).filter(models.Step.id == step_id).first()

    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_step.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db_step.step = step.step
    db_step.step_number = step.step_number

    db.commit()
    db.refresh(db_step)

    return db_step


@router.delete("/{step_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_step(
    step_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_step = db.query(models.Step).filter(models.Step.id == step_id).first()

    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_step.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(db_step)
    db.commit()

    return
