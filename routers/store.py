from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schema.storeschema import StoreCreate
router = APIRouter()


@router.post("/stores/add")
def add_store(store: StoreCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO stores (name, type , size , location) VALUES (%s,%s , %s, %s)",
                       (store.name, store.type , store.size ,store.location))
        conn.commit()
        return {"message": "Store added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/stores")
def list_stores():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, type , size ,  location FROM stores")
        rows = cursor.fetchall()
        return [{"id": r[0], "name": r[1], "type": r[2], "size": r[3], "location": r[4]} for r in rows]
    finally:
        cursor.close()
        conn.close()


# @router.post("/user/store")
# def select_store(user_id: int, store_id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "UPDATE users SET selected_store_id=%s WHERE id=%s", (store_id, user_id))
#         conn.commit()
#         return {"message": "Store selected"}
#     finally:
#         cursor.close()
#         conn.close()
