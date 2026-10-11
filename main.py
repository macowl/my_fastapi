from fastapi import FastAPI,Depends
from user.views import router as user_r
from my_site.views import router as user_r
from db import get_db,Base,engine
import uvicorn

app = FastAPI()

print("待创建表：", list(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)

app.include_router(user_r, prefix="/user")
app.include_router(user_r, prefix="/my_site")

@app.get("/")
def read_root(db = Depends(get_db)):
    return {"Hello": "World"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)