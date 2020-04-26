import datetime  # do not change this import, use datetime.datetime.now() to get date
from functools import wraps

#dekorator
def add_date(format):
  def wrap(func):
    @wraps(func)
    def neww(*args, **kwargs):
      result = func(*args, **kwargs)
      result['date']=datetime.datetime.now().strftime(format)
      return result
    return neww
  return wrap
#dekorator
def is_correct(*argu):
    def wrap(decorated):
        def wrapper(*args, **kwargs):
            result =decorated(*args, **kwargs)
            if all(arg in result for arg in argu):
                return result
            return None
        return wrapper
    return wrap
#dekorator
def wraps(to_be_decorated):
    def wrap(decorated):
        def wrapper(*args, **kwargs):
            return decorated(*args, **kwargs)
        wrapper.__name__ = to_be_decorated.__name__
        wrapper.__module__ = to_be_decorated.__module__
        wrapper.__doc__ = to_be_decorated.__doc__
        wrapper.__qualname__ = to_be_decorated.__qualname__
        wrapper.__annotations__ = to_be_decorated.__annotations__
        return wrapper
    return wrap



app.counter = 0
app.patients = []

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
def returns_delete():
    return {"method": "DELETE"}

@app.post("/patient", response_model=Patient_Resp)
def visit_patient(rq: Patient_Rq):
    app.patients.append(rq)
    app.counter += 1
    return Patient_Resp(id=app.counter,patient=rq)

@app.get("/patient/{pk}")
def informacje_patient(pk: int):
    if pk < len(app.patients):
        return app.patients[pk]
    else:
        return JSONResponse(status_code=204)
