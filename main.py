from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.counter = 0

class Patient_Rq(BaseModel):
    name: str
    surename: str

class Patient_Resp(BaseModel):
    id: int
    patient: Patient_Rq

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

@app.post("/patient", response_model=Patient_Resp)
def visit_patient(rq: Patient_Rq):
    app.counter += 1
    return Patient_Resp(id=app.counter,patient=rq)
