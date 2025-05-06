from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
from schema.userschema import User, UserCreate


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register")
def register(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(user.password)
        cursor.execute("INSERT INTO users (mobile, password) VALUES (%s, %s)",
                       (user.mobile, hashed_password))
        conn.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/token")
def login(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, password FROM users WHERE mobile=%s", (user.mobile,))
        result = cursor.fetchone()
        if not result or not pwd_context.verify(user.password, result[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = result[0]
        return {
            "access_token": user.mobile,
            "token_type": "bearer",
            "user_id": user_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/user/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT mobile FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"mobile": result[0]}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
