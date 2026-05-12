from fastapi import FastAPI, HTTPException, status, Depends
from models import User, Resource
from db import insert_user, check_user
from security import create_jwt_token
from depends import admin_auth, user_auth, guest_auth


app = FastAPI()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    if insert_user(user):
        return {"message": "New user created"}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists or invalid role")


@app.post("/login")
async def login(user: User):
    db_user = check_user(user)

    token = create_jwt_token(
        {
            "sub": db_user.username,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/protected_resource")
async def protected_resource(_ = Depends(user_auth)):
    return {"message": "Access granted"}


@app.post("/resources")
async def create_resource(resource: Resource, _ = Depends(admin_auth)):
    return {"message": "Resource created"}


@app.get("/resources")
async def get_resources(_ = Depends(guest_auth)):
    return {"message": "Resources list"}


@app.put("/resources/{resource_id}")
async def update_resource(resource_id: int, resource: Resource, _ = Depends(user_auth)):
    return {"message": "Resource updated"}


@app.delete("/resources/{resource_id}")
async def delete_resource(resource_id: int, _ = Depends(admin_auth)):
    return {"message": "Resource deleted"}