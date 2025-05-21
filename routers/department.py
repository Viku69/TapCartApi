from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schema.departmentschema import DepartmentCreate
router = APIRouter()


@router.post("/departments/add")
def add_department(department: DepartmentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO departments (name) VALUES (%s)",
                       (department.name,))
        conn.commit()
        return {"message": "Department added successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.get("/departments")
def list_departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM departments")
        rows = cursor.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]
    finally:
        cursor.close()
        conn.close()
