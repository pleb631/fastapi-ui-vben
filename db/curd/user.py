


def create_user(username: str, password: str):
    from db.models.user import User

    user = User(username=username, password=password)
    return user