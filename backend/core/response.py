from typing import Dict


def _res_antd(data: Dict = None, total: int = 0, code: bool = True):
    """
    支持ant-design-table 返回的格式
    """
    if data is None:
        data = {}
    result = {"success": code, "data": data, "total": total}
    return result


def _base_response(code, msg, data=None):
    if data is None:
        data = {}
    result = {"code": code, "message": msg, "data": data}
    return result


def success(data=None, msg=""):
    return _base_response(0, msg, data)


def fail(code=-1, msg="", data=None):
    return _base_response(code, msg, data)
