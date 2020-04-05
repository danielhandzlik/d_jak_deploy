from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def path_returns_HelloWorld():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/hello/{name}')
def hello_name(name: str):
    return {"message": f"Hello {name}"}
