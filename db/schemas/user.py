from sqlmodel import Field, SQLModel
from fastapi import Form

class UserCreate(SQLModel):

    username: str = Field(index=True, max_length=20, description="用户名")
    password: str = Field(max_length=255, description="密码")



    # 表单提交的数据是 application/x-www-form-urlencoded
    # FastAPI 默认会把 POST body 当成 JSON 来解析
    # 所以你定义参数为 userinfo: UserCreate（Pydantic 模型）时，FastAPI 以为前端发的是 JSON，而你发的是表单 → 格式不匹配

    # 如果是表单数据，需要用 Form() 来接收
    # async def result_page(
    #   req: Request,
    #   username: str = Form(...),
    #   password: str = Form(...)
    # ):...

    # 如果就想使用 Pydantic来接受表单数据，则需要转换，并用 Depends 注入
    # async def result_page(
    #     req: Request,
    #     userinfo: UserCreate = Depends(UserCreate.as_form),
    # ):

    @classmethod
    def as_form( 
            cls,
            username: str = Form(...),
            password: str = Form(...)
        ):
            return cls(username=username, password=password)

    # 如果想避免上述的写法，就只是想用Pydantic无脑接受数据，前端得改用ajax，走POST请求，并且要对返回的html进行手动写入
    
