# Importing the FastApi class
from fastapi import FastAPI
from typing import Optional
from enum import Enum
from pydantic import BaseModel


# creating model
class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


# creating Item
class Item(BaseModel):
    name: str
    description: Optional['str'] = None
    price: float
    tax: Optional[float] = None


# Creating an app object
app = FastAPI()
# query parameters
fake_items_db = [{'item_name': 'Foo'}, {'item_name': 'Bar'}, {'item_name': 'Baz'}]


# Lien dev
@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {'item_id': item_id, **item.dict()}
    return {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}
    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}
    return {'model_name': model_name, 'message': 'Have some residuals'}


'''Path Parameters'''

# @app.get('/items/{item_id}')
# async def read_item(item_id: int) -> dict:
#     return {'item_id': item_id}

'''optional parameters'''


@app.get('/items/{item_id}')
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False) -> dict:
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long '})
    return item


'''Path convertor'''


@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


'''Pydantic'''


@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


'''query parameter'''


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip:skip + limit]


# end Lien Dev
# Default route

# A minimal app to demonstrate the get request
@app.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}


# GET -- > Read Todo
@app.get("/todo", tags=['Todos'])
async def get_todos() -> dict:
    return {"Data": todos}


# Post -- > Create Todo
@app.post("/todo", tags=["Todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": "A Todo is Added!"
    }


# PUT  -- > Update Todo
@app.put("/todo/{id}", tags=["Todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if (int(todo["id"])) == id:
            todo["Activity"] = body["Activity"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
    return {
        "data": f"This Todo with id {id} is not found!"
    }


# DELETE --> Delete Todo
@app.delete("/todo/{id}", tags=["Todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been deleted!"
            }
    return {
        "data": f"Todo with id {id} was not found!"
    }


# Todos List

todos = [
    {
        "id": "1",
        "Activity": "Jogging for 2 hours at 7:00 AM."
    },
    {
        "id": "2",
        "Activity": "Writing 3 pages of my new book at 2:00 PM."
    }
]
