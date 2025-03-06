from fastapi import FastAPI

app = FastAPI()

test_db = [
    {"item_name": "Foo1"}, {"item_name": "Bar2"}, {"item_name": "Baz3"},
    {"item_name": "Foo4"}, {"item_name": "Bar5"}, {"item_name": "Baz6"},
    {"item_name": "Foo7"}, {"item_name": "Bar8"}, {"item_name": "Baz9"},
]


@app.post("/item/")
async def items(skip: int=0, limit: int=0):
    return test_db[skip : limit+2]