from fastapi import APIRouter, HTTPException
from typing import List
from schema.orderschema import Order
from database import get_db_connection
import uuid

router = APIRouter()



@router.post("/order/checkout")
def checkout(user_id: int, store_id: int):
    conn = get_db_connection()
    # use dictionary=True for clearer access
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Fetch cart items with product prices and stock
        cursor.execute("""
            SELECT p.id, p.price, p.stock_quantity, p.reorder_threshold, c.quantity
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        items = cursor.fetchall()

        if not items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # 2. Check stock availability
        for item in items:
            if item['quantity'] > item['stock_quantity']:
                raise HTTPException(status_code=400,
                                    detail=f"Not enough stock for product ID {item['id']}: only {item['stock_quantity']} left")

        # 3. Calculate total
        total_amount = sum(item['price'] * item['quantity'] for item in items)

        # ✅ 4. Generate UUID for order_id in Python
        order_uuid = str(uuid.uuid4())

        # 5. Insert order
        cursor.execute("INSERT INTO orders (user_id, order_id, total_amount, store_id) VALUES (%s, %s, %s, %s)",
                       (user_id, order_uuid, total_amount, store_id))

        # 6. Insert order items + update stock
        for item in items:
            # Insert order item
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (order_uuid, item['id'], item['quantity']))
            # Update stock quantity
            new_stock = item['stock_quantity'] - item['quantity']
            cursor.execute("UPDATE products SET stock_quantity = %s WHERE id = %s",
                           (new_stock, item['id']))

            # Optionally: Log if product hits low stock threshold
            if new_stock <= item['reorder_threshold']:
                print(
                    f"⚠️ Low stock alert for product ID {item['id']} (remaining: {new_stock})")

        # 7. Clear cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

        conn.commit()
        return {"message": "Order placed", "order_id": order_uuid, "total_amount": total_amount}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



@router.get("/orders/{user_id}")
def get_history(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id, order_id, total_amount, store_id, created_at
            FROM orders
            WHERE user_id=%s
            ORDER BY created_at DESC
            """, (user_id,))
        orders = cursor.fetchall()

        if not orders:
            raise HTTPException(
                status_code=404, detail="No orders found for this user")

        return [{
            "user_id": order[0],
            "order_id": order[1],
            "total_amount": order[2],
            "store_id": order[3],
            # optional formatting
            "created_at": order[4].strftime("%Y-%m-%d %H:%M:%S")
        } for order in orders]

    except Exception as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()



@router.get("/order/{order_id}/items")
def get_order_items(order_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.id, p.name, p.price, oi.quantity
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()

        if not items:
            raise HTTPException(
                status_code=404, detail="No items found for this order")

        return [{
            "product_id": row[0],
            "name": row[1],
            "price": row[2],
            "quantity": row[3],
            "total": row[2] * row[3]
        } for row in items]

    finally:
        cursor.close()
        conn.close()


@router.get("/verify-order/{order_id}")
def verify_order(order_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT order_id FROM orders WHERE order_id=%s", (order_id,))
        order = cursor.fetchone()
        if order:
            return {"status": "valid", "message": "Order is confirmed."}
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    finally:
        cursor.close()
        conn.close()
