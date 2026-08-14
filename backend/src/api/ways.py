from fastapi import APIRouter, Path
from fastapi.responses import FileResponse

router = APIRouter(tags=['ways'])


@router.get('/')
async def give_main_page():
    return FileResponse('static/index.html')

@router.get('/login')
async def give_login_page():
    return FileResponse('static/login.html')

@router.get('/register')
async def give_register_page():
    return FileResponse('static/register.html')


@router.get('/{user_name}')
async def give_home_page(user_name = Path()):
    return FileResponse('static/user_home.html')




