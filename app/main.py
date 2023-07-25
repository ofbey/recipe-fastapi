from fastapi import FastAPI
from .routers import recipe, ingredient, tag, step , nutrition, user, auth, like
from . import models
from .database import engine
# from . config import settings
# from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(recipe.router)
app.include_router(ingredient.router)
app.include_router(tag.router)
app.include_router(step.router)
app.include_router(nutrition.router)
app.include_router(like.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Recipe Fastapi"}


