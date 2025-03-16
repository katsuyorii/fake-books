from fastapi import APIRouter


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/register')
async def registration_user():
    pass