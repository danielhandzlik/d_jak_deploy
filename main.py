from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def path_returns_HelloWorld():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/GET')
def returns_get():
    return {"method": "GET"}

@app.post('/POST')
def returns_post():
    return {"method": "POST"}

@app.PUT('/PUT')
def returns_put():
    return {"method": "PUT"}

@app.delete('/DELETE')
def returns_get():
    return {"method": "DELETE"}
