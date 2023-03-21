from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
from flask import session

from app import oauth2
from app.database import User
from app.serializers.userSerializers import userEntity, userResponseEntity
from .. import schemas, utils
from app.oauth2 import AuthJWT
from ..config import settings

import requests

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib.parse import urljoin, urlencode

security = HTTPBearer()

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


templates = Jinja2Templates(directory="templates")

# @router.get("/")
# def login_page(request: Request):
#     return {"message": "Welcome to the login page"}


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, response: Response):
    # return templates.TemplateResponse("signup.html", {"request": request})
    return templates.TemplateResponse("logfin.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def signup_view(request: Request, response: Response):
    # return templates.TemplateResponse("signup.html", {"request": request})
    return templates.TemplateResponse("logfin.html", {"request": request})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# async def create_user(payload: schemas.CreateUserSchema):
async def create_user(response: Response, request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...),  confirm_password: str = Form(...,)):
    # Check if user already exist
    # user = User.find_one({'email': payload.email.lower()})
    user = User.find_one({'email': email})
    if user:
        email_exists = True
        # password_exists = True
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        #                     detail='Account already exist')
        return templates.TemplateResponse("logfin.html", {"request": request, "email_exists": email_exists})
    # Compare password and passwordConfirm
    if password != confirm_password:
        # if payload.password != payload.passwordConfirm:
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        return templates.TemplateResponse("logfin.html", {"request": request, "password_exists": "password_exists"})
    #  Hash the password
    # payload.password = utils.hash_password(payload.password)
    password = utils.hash_password(password)
    # del payload.passwordConfirm
    role = 'user'
    # payload.verified = True
    email = email.lower()
    # payload.created_at = datetime.utcnow()
    # payload.updated_at = payload.created_at
    # result = User.insert_one(payload.dict())
    result = User.insert_one(
        {"name": name, 'email': email, "password": password, "role": role})
    new_user = userResponseEntity(User.find_one({'_id': result.inserted_id}))
    # url =RedirectResponse("/api/auth/login") + f"#{message}"
    # return {"status": "success", "user": new_user}
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    # return RedirectResponse(url="/api/auth/login", status_code=status.HTTP_302_FOUND)
    # return RedirectResponse(url="/api/auth/login") + f"#{message}"
    # return RedirectResponse(url="/api/auth/login") 
    # message = "Your session has expired. Please log in again."
    # return templates.TemplateResponse("logfin.html", {"request": request}) 
 
 
    # return RedirectResponse(url=url)  
    # url = urljoin(app.url_path_for("login"), "?" + urlencode(query_params))

    # Redirect to the login page with the message
    return RedirectResponse(url=redirect_url)




@router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request, response: Response):
    return templates.TemplateResponse("logfin.html", {"request": request})
    # message = request.url.fragment
    # return {"message": message}


@router.post('/login')
# def login(payload: schemas.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends(),email: str = Form(...), password: str = Form(...)):
def login(request: Request,response: Response, Authorize: AuthJWT = Depends(), email: str = Form(...), password: str = Form(...)):
    # Check if the user exist
    # db_user = User.find_one({'email': payload.email.lower()})
    db_user = User.find_one({'email': email})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
        # return {"message": "Incorrect Email or Password"}
    user = userEntity(db_user)

    # Check if the password is valid
    if not utils.verify_password(password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
   
    context = {
        "request": request
    }
    # response = RedirectResponse("/api/users/me", status_code=status.HTTP_303_SEE_OTHER) # Post
    
    # response = RedirectResponse("/api/users/me",)      # POST Method
    response = RedirectResponse("/api/users/dashboard",status_code=status.HTTP_303_SEE_OTHER )  # GET Method

    # response.set_cookie(key="access_token", value=access_token)
    # return response

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

  
    # Send both access
    # return {'status': 'success', 'access_token': access_token}
    # return RedirectResponse(url='/api/auth/register', status_code=status.HTTP_303_SEE_OTHER )
    return response
    # return RedirectResponse(url="/api/auth/dash", status_code=status.HTTP_302_FOUND)
    # return RedirectResponse(url="/api/users/me", status_code=status.HTTP_302_FOUND)
    # res = RedirectResponse(url="/api/users/dashboard",status_code=status.HTTP_303_SEE_OTHER )
    # return res
    # return RedirectResponse(url='/api/auth/', status_code=status.HTTP_302_FOUND)



@router.get('/refresh11')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        # ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return RedirectResponse(url="/api/users/me", status_code=status.HTTP_302_FOUND)   


@router.get("/sss", response_class=HTMLResponse)
async def dash(request: Request,Authorize: AuthJWT = Depends()):
    # return templates.TemplateResponse("signup.html", {"request": request})
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(request: Request,response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    # return templates.TemplateResponse("dash.html", {"message": "Logged out successfully"})
    # return templates.TemplateResponse("logout.html", {"request": request, "alert1": f"Login successful", })       
    return RedirectResponse(url="/api/users/dashboardqq",)  

# @router.get("/logout", response_class=HTMLResponse)
# def login_get():
#     response = RedirectResponse(url="/")
#     response.delete_cookie(settings.COOKIE_NAME)
#     return response


    # session.pop("access_token", None)
    # response.delete_cookie('access_token')
    # return {'status': 'success'}
    # return templates.TemplateResponse("dash.html", {"request": request})
    # response = RedirectResponse("/",status_code=status.HTTP_303_SEE_OTHER)  # GET Method
    # return response


# @router.get('/logout', status_code=status.HTTP_200_OK)
# def logout(request: Request, response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
#     Authorize.unset_jwt_cookies()
#     response.set_cookie('logged_in', '', -1)
#     # return templates.TemplateResponse("login.html", {"request": request})
#     # return RedirectResponse(url="/login")
#     return {'status': 'success'}


# @router.get("/delete")
# def logout(response: Response):
#     response.delete_cookie("access_token")
#     # return {"message": "Logged out successfully"}
#     return RedirectResponse(url="/login")


# Delete access token cookie
def delete_access_token(response: RedirectResponse):
    response.delete_cookie('access_token')
    return response