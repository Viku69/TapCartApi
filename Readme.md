# TapCart API

TapCart is a scalable, modular e-commerce backend built with FastAPI. It provides robust features for user authentication, product and store management, cart operations, order processing, and sales analytics.

---

## 🚀 Features

- **User Authentication**: Secure registration and login using hashed passwords.
- **Product Management**: Add, retrieve, and manage products with QR code support.
- **Cart Operations**: Add, update, and remove items from the shopping cart.
- **Order Processing**: Checkout functionality with stock validation and order history.
- **Store & Department Management**: Manage store details and product departments.
- **Holiday Management**: Add and list holidays affecting sales.
- **Sales Analytics**: Download weekly sales data in CSV format.

---

## 📁 Project Structure

```
tapcart/
├── main.py
├── database/
│   └── connection.py
├── routers/
│   ├── auth.py
│   ├── cart.py
│   ├── orders.py
│   ├── products.py
│   ├── stores.py
│   ├── departments.py
│   ├── holidays.py
│   └── analytics.py
├── schemas/
│   ├── userschema.py
│   ├── productschema.py
│   ├── orderschema.py
│   └── ...
└── README.md
```

---

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/tapcart.git
   cd tapcart
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:

   Ensure you have a MySQL database named `tapcart` and update the `DATABASE_CONFIG` in `database/connection.py` accordingly.

5. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

---

## 📌 API Endpoints

### Authentication

- **Register**: `POST /register`
- **Login**: `POST /token`
- **Get User**: `GET /user/{user_id}`

### Cart

- **Add to Cart**: `POST /cart/add`
- **Update Cart**: `PUT /cart/update`
- **Remove from Cart**: `DELETE /cart/remove`
- **Get Cart**: `GET /cart/{user_id}`

### Orders

- **Checkout**: `POST /order/checkout`
- **Order History**: `GET /orders/{user_id}`
- **Order Items**: `GET /order/{order_id}/items`
- **Verify Order**: `GET /verify-order/{order_id}`

### Products

- **Add Product**: `POST /products/add`
- **List Products**: `GET /products`
- **Get Product by ID**: `GET /products/{product_id}`
- **Get Product by QR Code**: `GET /products/qr/{qr_code}`

### Stores

- **Add Store**: `POST /stores/add`
- **List Stores**: `GET /stores`

### Departments

- **Add Department**: `POST /departments/add`
- **List Departments**: `GET /departments`

### Holidays

- **Add Holiday**: `POST /add-holiday`
- **List Holidays**: `GET /holidays`

### Analytics

- **Download Weekly Sales**: `GET /download-weekly-sales`

---

## 📄 Schemas

Located in the `schemas/` directory, the Pydantic models define the structure of request and response bodies. Key schemas include:

- `UserCreate`
- `CartItem`
- `ProductCreate`
- `StoreCreate`
- `DepartmentCreate`
- `Holiday`

---



## 📚 Documentation

Once the application is running, access the interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 📌 Notes

- Ensure that the MySQL server is running and accessible.
- Replace default credentials in `database/connection.py` with secure values before deploying to production.
- Implement proper error handling and input validation for enhanced security.

---

## Authors

- Vikram Singh
- Varsha Raj
- Swati Verma
- Shivani Sharma