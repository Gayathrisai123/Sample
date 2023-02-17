from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates


app = FastAPI()
# client = MongoClient("mongodb://localhost:27017/")
# db = client["registration-db"]
# users = db["users"]

cluster = MongoClient('mongodb+srv://Gayathri:gayi@cluster0.iosmm7k.mongodb.net/?retryWrites=true&w=majority')
db = cluster["sample"]
users = db["123"]
templates =Jinja2Templates(directory="templates")


@app.get("/",response_class=HTMLResponse)
async def login(request: Request):
     return templates.TemplateResponse("ss.html",{"request": request})

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return """
        <html>
            <head>
                <title>Register</title>
            </head>
            <body>
                <h1>Register</h1>
                <form method="post">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                    <br>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                    <br>
                    <button type="submit">Register</button>
                </form>
            </body>
        </html>
    """


@app.post("/register", response_class=HTMLResponse)
async def do_register(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users.find_one({"username": username})
    if user:
        return "Username already exists."
    else:
        users.insert_one({"username": username, "password": password})
        return "Registration successful."


@app.post("/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users.find_one({"username": username})
    if user and user["password"] == password:
        return "Login successful."
    else:
        return "Invalid username or password."


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)