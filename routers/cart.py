from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import get_db_connection
from typing import List
from schema.cartschema import CartItem

router = APIRouter()



# class CartItem(BaseModel):
#     user_id: int
#     product_id: int
#     quantity: int


@router.post("/cart/add")
def add_to_cart(item: CartItem):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the item already exists in the cart
        cursor.execute(
            "SELECT quantity FROM cart WHERE user_id=%s AND product_id=%s",
            (item.user_id, item.product_id)
        )
        existing = cursor.fetchone()

        if existing:
            # If exists, update quantity by adding new quantity
            new_quantity = existing[0] + item.quantity
            cursor.execute(
                "UPDATE cart SET quantity=%s WHERE user_id=%s AND product_id=%s",
                (new_quantity, item.user_id, item.product_id)
            )
            message = "Cart quantity updated"
        else:
            # If not exists, insert new row
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                (item.user_id, item.product_id, item.quantity)
            )
            message = "Item added to cart"

        conn.commit()
        return {"message": message}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



@router.put("/cart/update")
def update_cart(item: CartItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE cart SET quantity=%s WHERE user_id=%s AND product_id=%s",
                       (item.quantity, item.user_id, item.product_id))
        conn.commit()
        return {"message": "Cart updated"}
    finally:
        cursor.close()
        conn.close()


@router.delete("/cart/remove")
def remove_from_cart(user_id: int, product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
        conn.commit()
        return {"message": "Item removed"}
    finally:
        cursor.close()
        conn.close()


@router.get("/cart/{user_id}", response_model=List[CartItem])
def get_cart(user_id: int):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT user_id, product_id, quantity FROM cart WHERE user_id=%s", (user_id,))
        items = cursor.fetchall()
        return [{"user_id": item[0], "product_id": item[1], "quantity": item[2]} for item in items]
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
