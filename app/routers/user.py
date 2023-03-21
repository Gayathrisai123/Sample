from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity

from app.database import User
from .. import schemas, oauth2


from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Form


router = APIRouter()
templates = Jinja2Templates(directory="templates")
template = Jinja2Templates(directory="template")

@router.post('/me', response_model=schemas.UserResponse)
async def get_me(request: Request,user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    # return {"status": "success", "user": user}
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/dashboard", response_model=schemas.UserResponse)
async def dashboard_post(request: Request,user_id: str = Depends(oauth2.require_user)):
    # Handle POST requests to the dashboard endpoint
    # return {"message": "You have posted to the dashboard!"}
    #  return templates.TemplateResponse("dashboard.html", {"request": request})
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    # return {"status": "success", "user": user}
    return templates.TemplateResponse("index2.html", {"request": request})

@router.get('/dashboardqq')
async def get_me(request: Request,user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    # return {"status": "success", "user": user}
    # return templates.TemplateResponse("signup.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})

# @router.get("/dash", response_class=HTMLResponse)
# async def dash(request: Request,user_id: str = Depends(oauth2.require_user)):
#     # return templates.TemplateResponse("signup.html", {"request": request})
#     return templates.TemplateResponse("dashboard.html", {"request": request})


