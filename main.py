from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def path_returns_HelloWorld():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/method')
def returns_get():
    return {"method": "GET"}

@app.post('/method')
def returns_post():
    return {"method": "POST"}

@app.put('/method')
def returns_put():
    return {"method": "PUT"}

@app.delete('/method')
def returns_get():
    return {"method": "DELETE"}
