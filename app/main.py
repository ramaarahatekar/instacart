from fastapi import FastAPI
from app.api.routes import departments, aisles , products, inventory, cart
from app.api.routes import checkout
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Instacart Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    departments.router,
    prefix="/departments",
    tags=["Departments"]
)
app.include_router(aisles.router, prefix="/aisles", tags=["Aisles"])

app.include_router(products.router, prefix="/products", tags=["Products"])

app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

app.include_router(cart.router, prefix="/cart", tags=["Cart"])

@app.get("/")
def health():
    return {"status": "backend running"}


app.include_router(
    checkout.router,
    prefix="/checkout",
    tags=["Checkout"]
)
