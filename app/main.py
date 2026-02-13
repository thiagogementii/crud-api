from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

DATA_FILE = "app/data.json"


def read_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def write_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# CREATE
@app.post("/users")
def create_user(user: dict):
    data = read_data()

    new_id = 1 if not data else data[-1]["id"] + 1
    user["id"] = new_id

    data.append(user)
    write_data(data)

    return user


# READ ALL
@app.get("/users")
def get_users():
    return read_data()


# READ ONE
@app.get("/users/{user_id}")
def get_user(user_id: int):
    data = read_data()

    for user in data:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: dict):
    data = read_data()

    for index, user in enumerate(data):
        if user["id"] == user_id:
            updated_user["id"] = user_id
            data[index] = updated_user
            write_data(data)
            return updated_user

    raise HTTPException(status_code=404, detail="User not found")


# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    data = read_data()

    for index, user in enumerate(data):
        if user["id"] == user_id:
            data.pop(index)
            write_data(data)
            return {"message": "User deleted"}

    raise HTTPException(status_code=404, detail="User not found")