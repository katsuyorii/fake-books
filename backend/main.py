from fastapi import FastAPI

from auth.router import auth_router
from users.router import users_router
from books.router import books_router


app = FastAPI()

app.include_router(books_router)
app.include_router(auth_router)
app.include_router(users_router)