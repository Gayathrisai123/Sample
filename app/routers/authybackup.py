from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException

from app import oauth2
from app.database import User
from app.serializers.userSerializers import userEntity, userResponseEntity
from .. import schemas, utils
from app.oauth2 import AuthJWT
from ..config import settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Request, Form


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN
# Configure templates directory
templates = Jinja2Templates(directory="templates")


@router.get("/signup", response_class=HTMLResponse)
async def signup_view(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(payload: schemas.CreateUserSchema, name: str = Form(...), email: str = Form(...), password: str = Form(...),  passwordConfirm: str = Form(...)):
    # sasync def create_user(payload: schemas.CreateUserSchema,username: str = Form(...), password: str = Form(...)):
    # Check if user already exist
    user = User.find_one({'email': email})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
        #  return {"message": "Account already exist"}
    # Compare password and passwordConfirm
    if password != passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        #  return {"message": "Passwords do not match"}
    #  Hash the password
    password = utils.hash_password(password)
    del payload.passwordConfirm
    # payload.role = 'user'
    # payload.verified = True
    email = email
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = User.insert_one(payload.dict())
    new_user = userResponseEntity(User.find_one({'_id': result.inserted_id}))
    # raise HTTPException(status_code=401, detail="user cretarednkbb.")
    return {"message": "Passwords do not match" , "user": new_user}
    # return {"status": "success", "user": new_user}
# raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse("logfin.html", {"request": request})

@router.post('/login')
def login( response: Response, Authorize: AuthJWT = Depends(),email: str = Form(...), password: str = Form(...)):
    # Check if the user exist
    # db_user = User.find_one({'email': payload.email.lower()})
    db_user = User.find_one({'email': email})
    if not db_user:
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        #                     detail='Incorrect Email or Password')
        return {"message": "Incorrect Email or Password"}
    user = userEntity(db_user)

    # Check if the password is valid
    if not utils.verify_password(password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

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
    return {"message": "user login sucessfully"}


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
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'success'}
