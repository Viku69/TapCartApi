from fastapi import FastAPI , APIRouter
from schema.holidayschema import Holiday
from database import get_db_connection

router = APIRouter()


@router.get("/holidays")
def list_holidays():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT date, name FROM holidays ORDER BY date ASC")
    holidays = cursor.fetchall()
    conn.close()
    return holidays

@router.post("/add-holiday")
def add_holiday(holiday: Holiday):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO holidays (date, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = %s"
    cursor.execute(query, (holiday.date, holiday.name, holiday.name))
    conn.commit()
    conn.close()
    return {"message": "Holiday added or updated successfully"}
