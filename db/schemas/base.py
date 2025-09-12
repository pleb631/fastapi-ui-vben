from sqlmodel import SQLModel, Field


class BaseResp(SQLModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")
