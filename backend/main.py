from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Mock data for demonstration
products = []
users = []
inquiries = []
carts = {}

# Models
class Product(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: float

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class User(BaseModel):
    id: int
    username: str
    email: str

class Inquiry(BaseModel):
    user_id: int
    message: str

class CartItem(BaseModel):
    product_id: int
    quantity: int

# Product Endpoints
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    new_id = len(products) + 1
    new_product = Product(id=new_id, **product.dict())
    products.append(new_product)
    return new_product

@app.get("/products/", response_model=List[Product])
async def get_products():
    return products

@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate):
    index = next((i for i, p in enumerate(products) if p.id == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(id=product_id, **product.dict())
    products[index] = updated_product
    return updated_product

@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    index = next((i for i, p in enumerate(products) if p.id == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products.pop(index)
    return {"message": "Product deleted successfully"}

# User Endpoints (simplified)
@app.post("/users/")
async def create_user(user: User):
    users.append(user)
    return user

# Inquiry Endpoints
@app.post("/inquiries/")
async def create_inquiry(inquiry: Inquiry):
    inquiries.append(inquiry)
    return inquiry

# Cart Endpoints
@app.post("/cart/{user_id}/")
async def add_to_cart(user_id: int, item: CartItem):
    if user_id not in carts:
        carts[user_id] = []
    carts[user_id].append(item)
    return carts[user_id]

@app.get("/cart/{user_id}/", response_model=List[CartItem])
async def get_cart(user_id: int):
    return carts.get(user_id, [])

@app.delete("/cart/{user_id}/{product_id}")
async def remove_from_cart(user_id: int, product_id: int):
    if user_id in carts:
        carts[user_id] = [item for item in carts[user_id] if item.product_id != product_id]
    return carts[user_id]
