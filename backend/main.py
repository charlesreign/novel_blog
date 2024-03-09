import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from database import models
from database.database import engine
from routers import post
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()

api.include_router(post.router)


models.Base.metadata.create_all(engine)

api.mount('/images', StaticFiles(directory='images'), name='images')

origin = [
  'http://localhost:3000'
]

api.add_middleware(
  CORSMiddleware,
  allow_origins=origin,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)