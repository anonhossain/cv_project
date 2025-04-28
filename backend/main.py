from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dbhelper import DBhelper
from api.views import api

app = FastAPI()

origins = ["http://127.0.0.1:5500/frontend/"]
# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api)
db = DBhelper()  # Create an instance of DBhelper

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",  # Use localhost IP address
        port=8080,
        reload=True
    )
