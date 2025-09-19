import hashlib
import uuid
import json
import functools
from typing import Callable, Any, Dict, Hashable, List, Optional
from core.redis import redis_client
from passlib.handlers.pbkdf2 import pbkdf2_sha256


def random_str():
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding="UTF-8")).hexdigest()
    return str(only)


def cacheable(ttl: int = 3600, key_prefix: str = "cache"):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"

            cached = await redis_client.get(key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await redis_client.set(key, json.dumps(result, default=str), ex=ttl)

            return result

        return wrapper

    return decorator


def en_password(psw: str):

    password = pbkdf2_sha256.hash(psw)
    return password


def check_password(password: str, old: str):

    check = pbkdf2_sha256.verify(password, old)
    if check:
        return True
    else:
        return False


def build_tree(
    rows: List[Dict[str, Any]],
    *,
    id_key: str = "key",
    parent_key: str = "parent_id",
    children_key: str = "children",
    root_parent: Optional[Hashable] = 0,  # 根的 parent_id（如用 None 就填 None）
    keep_fields: Optional[List[str]] = None,  # 只保留这些字段；None 则保留全部
    sort_key: Optional[str] = None,  # 可选：按某个字段排序
    prune_empty_children: bool = True,  # True: 去掉空 children
) -> List[Dict[str, Any]]:
    # 1) 拷贝并建节点映射，避免修改原 rows
    nodes: Dict[Hashable, Dict[str, Any]] = {}
    for r in rows:
        node = {k: r[k] for k in (keep_fields or r.keys()) if k in r}
        node.setdefault(children_key, [])  # 先占位，后面好统一追加
        nodes[r[id_key]] = node

    # 2) 组装父子关系
    forest: List[Dict[str, Any]] = []
    for r in rows:
        node = nodes[r[id_key]]
        pid = r.get(parent_key)
        if pid == root_parent or pid not in nodes:
            forest.append(node)  # 根节点（或找不到父亲的“孤儿”）
        else:
            nodes[pid][children_key].append(node)

    # 3) 可选：递归排序
    if sort_key:

        def sort_rec(lst: List[Dict[str, Any]]):
            lst.sort(key=lambda x: x.get(sort_key))
            for n in lst:
                sort_rec(n[children_key])

        sort_rec(forest)

    # 4) 可选：去掉空 children
    if prune_empty_children:
        for n in nodes.values():
            if not n[children_key]:
                n.pop(children_key, None)

    return forest
