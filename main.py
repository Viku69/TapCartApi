from fastapi import FastAPI , HTTPException
from database import get_db_connection
from routers import auth , cart , orders , store , product , department , holiday , getcsv 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Routes
@app.get("/")
def welcome():
    return "Welcome to the TapCart API"


app.include_router(auth.router, tags=["Authentication"])
app.include_router(cart.router, tags=["Cart"])
app.include_router(orders.router, tags=["Orders"])
app.include_router(store.router, tags=["Store"])
app.include_router(product.router, tags=["Product"])
app.include_router(department.router, tags=["Department"])
app.include_router(holiday.router, tags=["Holiday"])
app.include_router(getcsv.router, tags=["Get_Weekly_Sales_Data"])
