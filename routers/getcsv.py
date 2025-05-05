from fastapi import APIRouter, HTTPException , Response
from typing import List
from schema.orderschema import Order
from database import get_db_connection
import io , csv

router = APIRouter()


@router.get("/download-weekly-sales")
def download_weekly_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT
            o.store_id AS Store,
            s.size AS Size,
            s.type AS Type,
            p.department_id AS Dept,
            YEAR(o.created_at)  AS Year,
            WEEK(o.created_at, 1) AS Week,
            CASE WHEN COUNT(h.date) > 0 THEN 'TRUE' ELSE 'FALSE' END AS isHoliday,
            SUM(oi.quantity * p.price) AS weekly_sales
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        JOIN stores s ON o.store_id = s.id
        LEFT JOIN holidays h ON DATE(o.created_at) = h.date
        GROUP BY o.store_id, s.size, s.type, p.department_id, year, week
        ORDER BY o.store_id, p.department_id, year, week;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Store', 'Size', 'Type', 'Dept',
                         'Year', 'Week', 'isHoliday', 'weekly_sales'])

        for row in results:
            writer.writerow(row)

        response = Response(content=output.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=weekly_sales.csv"
        return response

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
