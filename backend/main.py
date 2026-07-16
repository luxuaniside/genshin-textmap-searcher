from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.read_services import search_query

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://luxuani-textmap-searcher.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from Luxuani!"}


@app.get("/search/{text}")
def search_text_query(text: str):
    return search_query(text)