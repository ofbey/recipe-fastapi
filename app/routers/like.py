from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/like",
    tags=['Like']
)

# 1 for adding like , 0 for removing like

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: schemas.Like,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == like.recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Recipe with id: {like.recipe_id} does not exist")

    db_like = db.query(models.Like).filter(
        models.Like.recipe_id == like.recipe_id, models.Like.user_id == current_user.id)

    found_like = db_like.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy liked recipe {like.recipe_id}")
        new_like = models.Like(recipe_id=like.recipe_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        db_like.delete(synchronize_session=False)
        db.commit()

        return {"message": "like successfully removed"}
