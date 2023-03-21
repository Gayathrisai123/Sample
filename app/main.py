from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.config import settings
from app.routers import auth, user

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(HTTPException)
async def redirect_to_login(request: Request, exc: HTTPException) -> Response:
         # pylint: disable=unused-argument
    if exc.status_code == 401:
        # Redirect to login page
        return HTMLResponse("<script>window.location.href = '/';</script>")
    # Re-raise the exception for other status codes
    raise exc

templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, tags=['Auth'], prefix='')
app.include_router(user.router, tags=['Users'], prefix='/api/users')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}

