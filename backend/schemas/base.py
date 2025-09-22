from sqlmodel import SQLModel, Field
from typing import Optional, Any

class BaseResp(SQLModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")


class WebsocketMessage(SQLModel):
    action: Optional[str]
    user: Optional[int] = None
    data: Optional[Any] = None
    content: Optional[str] = None
    t: Optional[int] = None