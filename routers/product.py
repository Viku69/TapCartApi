from fastapi import APIRouter, HTTPException
from database import get_db_connection
from typing import List
from schema.productschema import ProductCreate , Product
router = APIRouter()


@router.post("/products/add")
def add_product(product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, price, qr_code , department_id) VALUES (%s, %s, %s , %s)",
                       (product.name, product.price, product.qr_code , product.department_id))
        conn.commit()
        return {"message": "Product added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Endpoint to get all products


@router.get("/products", response_model=List[Product])
def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # To return results as dictionaries
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/products/{product_id}")
def get_product_by_product_id(product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, name, price , department_id FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product[0], "name": product[1], "price": product[2], "department_id": product[3]}
    finally:
        cursor.close()
        conn.close()


@router.get("/products/qr/{qr_code}")
def get_product_by_qr(qr_code: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, name, price , department_id FROM products WHERE qr_code=%s", (qr_code,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product[0], "name": product[1], "price": product[2], "department_id": product[3]}
    finally:
        cursor.close()
        conn.close()
