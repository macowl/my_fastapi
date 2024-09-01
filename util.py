import bcrypt
from fastapi import Request,Header,HTTPException
import jwt

# 加密密码的函数  
def hash_password(password):  
    salt = bcrypt.gensalt()  
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
  
# 验证密码的函数  
def check_password(hashed_password, user_password):  
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))  



def verify_headers(x_token: str = Header(...)):
    try:
        res = jwt.decode(x_token, "secret", algorithms=["HS256"])
        return res["username"]
    except:
        raise HTTPException(status_code=400, detail="错误")