from fastapi import FastAPI,Depends
from user.views import router as user_r
from db import get_db

import uvicorn
app = FastAPI()

app.include_router(user_r, prefix="/user")

@app.get("/")
def read_root(db = Depends(get_db)):
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)