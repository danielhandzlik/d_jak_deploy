#from fastapi import FastAPI
#from pydantic import BaseModel
#from fastapi.responses import JSONResponse
#
#app = FastAPI()
#app.counter = 0
#app.patients = []
#
#class Patient_Rq(BaseModel):
#    name: str
#    surename: str
#
#class Patient_Resp(BaseModel):
#    id: int
#    patient: Patient_Rq
#
#@app.get('/')
#def path_returns_HelloWorld():
#    return {"message": "Hello World during the coronavirus pandemic!"}
#
#@app.get('/method')
#def returns_get():
#    return {"method": "GET"}
#
#@app.post('/method')
#def returns_post():
#    return {"method": "POST"}
#
#@app.put('/method')
#def returns_put():
#    return {"method": "PUT"}
#
#@app.delete('/method')
#def returns_delete():
#    return {"method": "DELETE"}
#
#@app.post("/patient", response_model=Patient_Resp)
#def visit_patient(rq: Patient_Rq):
#    app.patients.append(rq)
#    app.counter += 1
#    return Patient_Resp(id=app.counter,patient=rq)

#@app.get("/patient/{pk}")
#def informacje_patient(pk: int):
#    if pk < len(app.patients):
#        return app.patients[pk]
#    else:
#        return JSONResponse(status_code=204)
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
app.ID = 0
app.patients = {}
app.session_tokens = []
app.secret_key = "kdajdksnaldadowndmadk3213mnd2qeq2m2k32am22d2q2das2ky6678asdgrWED"


from fastapi.templating import Jinja2Templates
from fastapi import Cookie, Request

templates = Jinja2Templates(directory="templates")

@app.get("/welcome")
def do_welcome(request: Request, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	return templates.TemplateResponse("item.html", {"request": request, "user": "trudnY"})


from hashlib import sha256
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, Response, status
import secrets

security = HTTPBasic()


@app.post("/login")
def get_current_user(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.session_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND 


@app.post("/logout")
def logout(*, response: Response, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	app.session_tokens.remove(session_token)
	return RedirectResponse("/")

@app.post("/patient")
def add_patient(response: Response, patient: PatientRq, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	if app.ID not in app.patients.keys():
		app.patients[app.ID] = patient.dict()
		app.ID += 1
	response.set_cookie(key="session_token", value=session_token)
	response.headers["Location"] = f"/patient/{app.ID-1}"
	response.status_code = status.HTTP_302_FOUND

@app.get("/patient")
def display_patients(response: Response, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens:
		raise HTTPException(status_code=401, detail="Unathorised")
	return app.patients
    

@app.get("/patient/{id}")
def display_patient(response: Response, id: int, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens: 
		raise HTTPException(status_code=401, detail="Unathorised")
	response.set_cookie(key="session_token", value=session_token)
	if id in app.patients.keys():
		return app.patients[id]

@app.delete("/patient/{id}")
def delete_patient(response: Response, id: int, session_token: str = Cookie(None)):
	if session_token not in app.session_tokens: 
		raise HTTPException(status_code=401, detail="Unathorised")
	app.patients.pop(id, None)		
	response.status_code = status.HTTP_204_NO_CONTENT

