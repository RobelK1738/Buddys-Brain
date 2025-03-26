from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import resources, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(resources.router)
app.include_router(search.router)
