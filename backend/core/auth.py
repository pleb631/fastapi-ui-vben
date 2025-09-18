from fastapi import Request
from fastapi.security import SecurityScopes
from datetime import timedelta, datetime, UTC
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from starlette import status
from jwt import PyJWTError
from pydantic import ValidationError
from typing import List


from models.base import Access
from config import settings
import curd
from core.session import SessionDep


oauth = OAuth2PasswordBearer(
    settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
    scheme_name="User",
    scopes={"is_admin": "超级管理员", "not_admin": "普通管理员"},
)


def create_access_token(data: dict):
    token_data = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data.update({"exp": expire})

    jwt_token = jwt.encode(
        token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return jwt_token


async def check_permissions(
    req: Request,
    security_scopes: SecurityScopes,
    session: SessionDep,
    token=Depends(oauth),
):

    try:

        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        if payload:
            user_id = payload.get("user_id", None)
            user_type = payload.get("user_type", None)

            if user_id is None or user_type is None:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer {token}"},
                )
                raise credentials_exception

        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
            raise credentials_exception

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已证过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    except (PyJWTError, ValidationError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    except jwt.ExpiredSignatureError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已经过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    check_user = await curd.user.get_user(session, user_id=user_id)
    if not check_user or check_user.user_status != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已经被管理员禁用!",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    if security_scopes.scopes:
        print("当前域：", security_scopes.scopes)

        scopes: List[Access] = []
        if not user_type and security_scopes.scopes:
            scopes: List[Access] = await curd.user.get_user_rules(
                session, user_id=check_user.id
            )

            if not scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="用户没有权限!",
                    headers={"WWW-Authenticate": f"Bearer {token}"},
                )
            for scope in security_scopes.scopes:
                if scope not in [s.scopes for s in scopes]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="用户没有权限!",
                        headers={"WWW-Authenticate": f"Bearer {token}"},
                    )
            req.state.scopes = scopes

    req.state.user_id = user_id
    req.state.user_type = user_type
