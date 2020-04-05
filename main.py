from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def path_returns_HelloWorld():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/{method}')
def returns_method(method: str):
    return {"method": f"{method}"}