from uuid import uuid4, UUID
from typing import List

from fastapi import FastAPI, HTTPException

from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("c969a793-6e52-4555-af5f-62f41783f9a4"),
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        email="john@example.com",
        roles=[Role.student]
    ),
    User(
        id=UUID("63284b06-f0a4-4c11-a4fd-b8b73c27141d"),
        first_name="Marina",
        last_name="Melek",
        gender=Gender.female,
        email="m93@example.com",
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/api/v1/users")
async def get_users():
    return {"users": db}


@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return {"message": "User has been created successfully!",
            "user": user}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User has been deleted successfully!"}
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist!")


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.roles is not None:
                user.roles = user_update.roles
            return {"message": "User has been updated successfully!"}
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} does not exist!")
