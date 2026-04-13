from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="A simple API with GET and POST endpoints",
    version="1.0.0"
)

# Data model for items
class Item(BaseModel):
    id: int
    name: str
    description: str = None
    price: float

# In-memory database
items_db = [
    {"id": 1, "name": "Item 1", "description": "First item", "price": 9.99},
    {"id": 2, "name": "Item 2", "description": "Second item", "price": 19.99}
]

@app.get("/")
def get_home_page():
    """Home page - returns a welcome message"""
    return {"message": "This is home page", "status": "success"}

@app.get("/authentication")
def get_authentication():
    """
    Authentication reachability check.

    Returns:
        str: The plain string "authenticated" with HTTP 200 and Content-Type: application/json
    """
    return JSONResponse(content="authenticated", status_code=200)

@app.get("/items")
def get_all_items():
    """
    Get all items.
    
    Returns:
        list: A list of all items in the database
    """
    return {"items": items_db, "count": len(items_db)}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Get a specific item by ID.
    
    Parameters:
        item_id: The unique identifier of the item
    
    Returns:
        dict: The item details or an error message if not found
    """
    for item in items_db:
        if item["id"] == item_id:
            return {"data": item, "status": "success"}
    return {"error": "Item not found", "status": "error"}

@app.post("/items")
def create_item(item: Item):
    """
    Create a new item.
    
    Parameters:
        item: The item details (name, description, price)
    
    Returns:
        dict: The created item with its ID
    """
    new_item = {
        "id": max([i["id"] for i in items_db], default=0) + 1,
        "name": item.name,
        "description": item.description,
        "price": item.price
    }
    items_db.append(new_item)
    return {"data": new_item, "message": "Item created successfully", "status": "success"}