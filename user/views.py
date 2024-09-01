from fastapi import APIRouter,Depends
from db import get_db
import jwt
from .models import User_data,User
from util import hash_password,check_password,verify_headers


router = APIRouter()



@router.get("/")
def index(username: str = Depends(verify_headers)):          # 请求头携带token进行验证，x—token
    return username


@router.post("/register") 
def register(User_data:User_data,db = Depends(get_db)):
    password_hash = hash_password(User_data.password)                           # 生成hash密码
    new_user = User(username=User_data.username,password_hash = password_hash)
    db.add(new_user)
    try:
        db.commit()                                                             # 保存密码
        return True
    except:
        return False


@router.post("/login")
def login(user_data:User_data,db = Depends(get_db)):
    user = db.query(User).filter_by(username=user_data.username).first()
    if user and check_password(user.password_hash,user_data.password):          # 核对密码
        encoded = jwt.encode({"username": user_data.username}, "secret", algorithm="HS256")
        return {"token": encoded}                                               # 返回token
    else:
        return False