import time
from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect
from jwt import PyJWTError
from pydantic import ValidationError
import jwt
from typing import Any
from sqlmodel import select

from config import settings
from models.base import User
from schemas.base import WebsocketMessage
from core.session import async_session_maker


websocket_router = APIRouter(prefix="/ws", tags=["WebSocket"])


def check_token(token: str):
    try:
        # token解密
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload:
            # 用户ID
            uid = payload.get("user_id", 0)
            if uid == 0:
                return False
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except (PyJWTError, ValidationError):
        return False
    return uid


@websocket_router.websocket_route("/test")
class Echo(WebSocketEndpoint):
    encoding = "json"
    active_connections = []

    # WebSocket 连接
    async def on_connect(self, web_socket: WebSocket):
        u_type = web_socket.query_params.get("u_type")
        token = web_socket.headers.get("sec-websocket-protocol")
        real_ip = web_socket.headers.get("origin")
        real_host = web_socket.headers.get("host")

        try:

            if not u_type or not token:
                raise WebSocketDisconnect
            u_id = check_token(token)
            if not u_id:
                raise WebSocketDisconnect
            await web_socket.accept(subprotocol=token)

            for con in self.active_connections:
                if con["u_id"] == u_id and con["u_type"] == u_type:
                    self.active_connections.remove(con)
            print(
                f"客户端ip:{real_ip} 来源:{real_host} type:{int(u_type)} ID: {int(u_id)}"
            )

            self.active_connections.append(
                {"u_type": int(u_type), "u_id": int(u_id), "con": web_socket}
            )
            u_ids = [i["u_id"] for i in self.active_connections]
            if u_ids:
                async with async_session_maker() as session:
                    async with session.begin():
                        stmt = select(User.id.label("id"), User.username.label("username"), User.avatar.label("avatar")).where(
                            User.id.in_(u_ids)
                        )
                        result = await session.execute(stmt)

                        online_user = result.mappings().all()
                        online_user = [dict(i) for i in online_user]

            else:
                online_user = []

            data = {"action": "refresh_online_user", "data": online_user}
            time.sleep(0.5)
            print(self.active_connections)
            for con in self.active_connections:
                await con["con"].send_json(data)
        except WebSocketDisconnect:
            await web_socket.close()
            print("断开了连接")
 
    # WebSocket 消息接收
    async def on_receive(self, web_socket: WebSocket, msg: Any):
        try:
            token = web_socket.headers.get("Sec-Websocket-Protocol")
            user = check_token(token)
            if user:
                msg = WebsocketMessage(**msg)
                action = msg.action
                if action == "push_msg":
                    # 群发消息
                    for i in self.active_connections:
                        msg.action = "pull_msg"
                        msg.user = user
                        await i["con"].send_json(msg.model_dump())
                elif action == "ping":
                    # 可选：直接忽略或回 pong
                    # await web_socket.send_json({"action": "pong", "t": ws_msg.t})
                    return

            else:
                raise WebSocketDisconnect
        except Exception as e:
            print(e)

    async def on_disconnect(self, web_socket, close_code):
        print(web_socket,self.active_connections)
        for con in self.active_connections:
            if con["con"] == web_socket:
                
                self.active_connections.remove(con)
            u_ids = [i["u_id"] for i in self.active_connections]
            if u_ids:
                async with async_session_maker() as session:
                    async with session.begin():
                        stmt = select(User.id.label("id"), User.username.label("username"), User.avatar.label("avatar")).where(
                            User.id.in_(u_ids)
                        )
                        result = await session.execute(stmt)

                        online_user = result.mappings().all()
                        online_user = [dict(i) for i in online_user]

            else:
                online_user = []
        data = {"action": "refresh_online_user", "data": online_user}
        for con in self.active_connections:
            await con["con"].send_json(data)

    # async def send_message(self,
    #                        web_socket: WebSocket,
    #                        sender: int,
    #                        sender_type: int,
    #                        recipient: int,
    #                        recipient_type: int,
    #                        data: dict):
    #     """
    #     消息发送
    #     :param web_socket: 发送者连接对象
    #     :param sender: 发送者ID
    #     :param sender_type: 发送者用户类型
    #     :param recipient: 接收者用户ID
    #     :param recipient_type: 接收者用户类型
    #     :param data: 要发送的数据
    #     :return:
    #     """
    #     is_online = False  # 用户在线状态
    #     for con in self.active_connections:
    #         # 找到到对方
    #         if con["u_id"] == recipient and con["u_type"] == recipient_type:
    #             is_online = True
    #             message = {
    #                 "sender": sender,
    #                 "sender_type": sender_type,
    #                 "data": data
    #             }
    #             print(data)
    #             await con["con"].send_text(json.dumps(message))
    #     # 用户是否在线
    #     if is_online:
    #         await web_socket.send_text('{"send_status":"send-success"}')
    #     else:
    #         await web_socket.send_text('{"send_status":"send-fail"}')
