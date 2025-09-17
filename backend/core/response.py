from typing import Dict


def _base_response(code, msg, data=None):
    result = {"code": code, "message": msg, "data": data}
    return result


def success(data=None, msg=""):
    return _base_response(0, msg, data)


def fail(code=-1, msg="", data=None):
    return _base_response(code, msg, data)
